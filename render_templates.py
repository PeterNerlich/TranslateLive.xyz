#!/usr/bin/env python3

import os
from pathlib import Path
from functools import lru_cache
import re
import datetime
import subprocess
import difflib
try:
	import icdiff
except ImportError:
	pass

DEBUG = not (os.environ.get("DEBUG", "False").lower() in ('false', 'f', 'no', 'n', '0', ''))

script_dir = os.path.dirname(os.path.realpath(__file__))
static_dir = Path(script_dir, "static")
template_dir = Path(script_dir, "templates")
render_dir = Path(script_dir, "docroot")

pattern = re.compile(r'(src|href)="([^"]*)"')


def make_render_url_fn(log_replaced=None, log_kept=None, debug=False):
	if log_replaced is None:
		log_replaced = []
	if log_kept is None:
		log_kept = []
	outer_debug = debug

	def render_url(match, debug=None):
		if debug is None:
			debug = outer_debug
		attr = match.group(1)
		url = match.group(2)
		# split off anchor and query part
		anchor_pos = url.index("#") if "#" in url else len(url)
		query_pos = url.index("?") if "?" in url else anchor_pos
		path = url[:query_pos]
		query = url[query_pos:anchor_pos]
		anchor = url[anchor_pos:]
		# no need replacing empty urls or those leading to external services
		if not url.strip() or url.startswith("http"):
			log_kept.append(url)
			if debug:
				print(f"not replacing external or empty url:  {url}")
			return match.group(0)
		# add timestamp to urls
		if path.endswith((".html", ".css", ".js", ".json")):
			timestamp = get_timestamp(path.removeprefix("/"), debug=debug)
			if query:
				query = f"{query}&v={timestamp}"
			else:
				query = f"?v={timestamp}"
		newurl = f"{path}{query}{anchor}"
		if url != newurl:
			log_replaced.append((url, newurl))
			if debug:
				print(f"replacing url: \t{url}\t→\t{newurl}")
		else:
			log_kept.append(url)
			if debug:
				print(f"not replacing url: \t{url}")
		return f'{attr}="{newurl}"'

	return render_url

@lru_cache(maxsize=1024)
def get_timestamp(url, debug=False):
	file = Path(template_dir, url)
	if not os.path.exists(file):
		if debug:
			print(f"get_timestamp({url!r}) Didn't exist in template dir: {file!r}")
		file = Path(render_dir, url)
	if os.path.isfile(file):
		timestamp = os.path.getmtime(file)
		value = datetime.datetime.fromtimestamp(timestamp).isoformat()
		if debug:
			print(f"get_timestamp({url!r}) Is a file: {file!r}  → {value!r}")
		return value
	else:
		print(f"get_timestamp({url!r}) Wasn't a file: {file!r}")

def compose_docroot(render_dir, template_dir, static_dir=None, debug=False):
	render_dir = Path(render_dir)
	if render_dir.exists():
		if not render_dir.is_dir():
			render_dir.unlink()
			render_dir.mkdir()
	else:
		render_dir.mkdir()

	if static_dir is not None:
		for static in Path(static_dir).rglob("*"):
			filename = os.path.relpath(static, static_dir)
			destination = Path(render_dir, filename)
			if static.is_dir():
				ensure_dir(destination, debug=debug)
			else:
				ensure_removal(destination)
				# create link
				#destination.symlink_to(static)
				destination.hardlink_to(static)
				# also set mtime from original
				stat = os.stat(static, follow_symlinks=False)
				os.utime(destination, (stat.st_atime, stat.st_mtime))

	# file stats
	written = []
	unchanged = []
	# link stats
	all_replaced = []
	all_kept = []
	for template in Path(template_dir).rglob("*"):
		replaced = []
		kept = []
		# read file
		filename = os.path.relpath(template, template_dir)
		destination = Path(render_dir, filename)
		# extract URIs
		rendered = pattern.sub(make_render_url_fn(replaced, kept, debug=debug), template.read_text())
		# write to dest
		if ensure_file(destination, rendered):
			written.append(destination)
		else:
			unchanged.append(destination)

		if not debug:
			print(f"rendered {filename}, replaced {len(replaced)} and kept {len(kept)} links (replaced {len(set(replaced))} and kept {len(set(kept))} unique links)")
		else:
			print(f"rendered {template} → {destination}\nreplaced {len(replaced)} and kept {len(kept)} links (replaced {len(set(replaced))} and kept {len(set(kept))} unique links)")
			nl = "\n\t"
			lines = map(lambda x: f"{x[1]} ×\t{repr(x[0])}", aggregate(replaced).items())
			print(f"  replaced:{nl}{nl.join(lines)}")
			lines = map(lambda x: f"{x[1]} ×\t{repr(x[0])}", aggregate(kept).items())
			print(f"  kept:{nl}{nl.join(lines)}")
		all_replaced.extend(replaced)
		all_kept.extend(kept)

	print(f"\nReplaced {len(all_replaced)} and kept {len(all_kept)} links in total (replaced {len(set(all_replaced))} and kept {len(set(all_kept))} unique links)")
	print(f"Written {len(written)} files, {len(unchanged)} unchanged")
	if debug:
		nl = "\n\t"
		lines = map(lambda x: f"{x[1]} ×\t{repr(x[0])}", aggregate(all_replaced).items())
		print(f"  replaced:{nl}{nl.join(lines)}")
		lines = map(lambda x: f"{x[1]} ×\t{repr(x[0])}", aggregate(all_kept).items())
		print(f"  kept:{nl}{nl.join(lines)}")

def aggregate(items):
	d = dict()
	for item in items:
		if item not in d:
			d[item] = 1
		else:
			d[item] += 1
	return d

def ensure_dir(path, debug=False):
	if path.exists():
		if not path.is_dir():
			if debug:
				print(f"ensure_dir({path!r}) Path exists as file (deleting)")
			path.unlink()
			path.mkdir()
		else:
			if debug:
				print(f"ensure_dir({path!r}) Directory already exists")
	else:
		if debug:
			print(f"ensure_dir({path!r}) Path didn't exist (creating directory)")
		path.mkdir()

def ensure_file(path, content, debug=False):
	if path.exists():
		if not path.is_file():
			#if debug:
			print(f"ensure_file({path!r}, content) Path exists as directory! (MANUAL ACTION REQUIRED)")
		else:
			with open(path, "r") as file:
				original = file.read()
				if original == content:
					if debug:
						print(f"ensure_file({path!r}, content) No changes to file content required")
					return False
				else:
					try:
						class Dummy:
							def __init__(self):
								self.cols = None
						options = Dummy()
						icdiff.set_cols_option(options)
						differ = icdiff.ConsoleDiff(
							cols=options.cols,
							line_numbers=True,
						).make_table(
							fromlines=original.split("\n"),
							tolines=content.split("\n"),
							fromdesc=f"{os.path.relpath(path, script_dir)}    {datetime.datetime.fromtimestamp(os.path.getmtime(path)).isoformat()}",
							todesc=f"{os.path.relpath(path, script_dir)}    {datetime.datetime.now().isoformat()}",
							context=True,
							numlines=3,
						)
					except NameError:
						differ = difflib.unified_diff(
							original.split("\n"),
							content.split("\n"),
							fromfile=str(os.path.relpath(path, script_dir)),
							tofile=str(os.path.relpath(path, script_dir)),
							fromfiledate=datetime.datetime.fromtimestamp(os.path.getmtime(path)).isoformat(),
							tofiledate=datetime.datetime.now().isoformat(),
						)

					for line in differ:
						print(line)
					print()
	with open(path, "w") as file:
		file.write(content)
	return True

def ensure_removal(path, debug=False):
	if path.exists():
		if path.is_file():
			if debug:
				print(f"ensure_removal({path!r}) Unlinking file")
			path.unlink()
		else:
			if debug:
				print(f"ensure_removal({path!r}) Removing directory")
			path.rmdir()
	else:
		if debug:
			print(f"ensure_removal({path!r}) Path already doesn't exist")

if __name__ == '__main__':
	git = Path(script_dir, ".git")
	version_global = Path(script_dir, "version.json")
	version_target = Path(render_dir, "version.json")
	if git.exists() and git.is_dir():
		proc = subprocess.run([Path(script_dir, "save_version_json.sh"), "--"], capture_output=True)
		content = proc.stdout.decode("utf-8")
		ensure_file(version_target, content)
	elif version_global.exists() and version_global.is_file():
		version_global.copy(version_target)
		print("No .git directory, copied global version.json")
	else:
		print("Unable to generate version file! No .git directory and no global version.json")

	compose_docroot(render_dir=render_dir, template_dir=template_dir, static_dir=static_dir, debug=DEBUG)
