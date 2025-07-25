#!/usr/bin/env python3

import os
import asyncio
import datetime
import websockets
import logging
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from transcript import Session, Transcript, Line
from translator import DeepLTranslator, DummyTranslator
from util import version

logging.basicConfig(
	filename='server.log',
	encoding='utf-8',
	format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
	level=logging.DEBUG,
)
logger = logging.getLogger(f"{__name__}.handler")
logger.setLevel(logging.DEBUG)
log_handler = logging.FileHandler(filename=f"server.handler.log", encoding="utf-8")
log_handler.setFormatter(logging.Formatter(fmt='%(asctime)s [%(name)s] %(levelname)s: %(message)s'))
logger.addHandler(log_handler)

SEP = " "
QUOTE = chr(27) # Escape
DUMMY = not (os.environ.get("DUMMY", "False").lower() in ('false', 'f', 'no', 'n', '0', ''))

default_session = Session(name="default")
languages = ["de", "uk", "en", "ro"]
transcripts = {}
for language in languages:
	transcripts[language] = Transcript(language)
	default_session.add_transcript(transcripts[language])

Translator = (
	DummyTranslator
	if DUMMY else
	DeepLTranslator
)
if Translator is DummyTranslator:
	logger.warning("Using DummyTranslator! (%s)", repr(os.environ.get('DUMMY')))
	print(f"Using DummyTranslator! ({repr(os.environ.get('DUMMY'))})")

translators = {
	"uk": Translator(transcripts["de"], transcripts["uk"], paused=True),
	"en": Translator(transcripts["de"], transcripts["en"], paused=True),
	"ro": Translator(transcripts["de"], transcripts["ro"], paused=True),
}

clients = set()
connected = set()
sessions = set([default_session])

def save_session_srt(session):
	date = datetime.datetime.fromtimestamp(session.date).isoformat()
	now = datetime.datetime.now().isoformat()
	logger.info("Stopped server. Saving transcripts as %s_%s.*.srt", date, now)
	for language, transcript in session.transcripts.items():
		with open(f"{date}_{now}.{session.name}.{language}.srt", "w") as outfile:
			outfile.write(transcript.to_srt())

import atexit
atexit.register(lambda: save_session_srt(default_session))

# channels[role][session][language] = set(websockets)
channels = {
	"reader": {},
	"source": {},
	"editor": {},
}

def broadcast_update(message_fn: callable, role=None, session=None, language=None):
	def matching(dictionaries: list[dict], selector = None):
		if type(dictionaries) is not list:
			dictionaries = [dictionaries]
		return [
			v
			for d in dictionaries
			for k,v in d.items()
			if selector is None or k == selector or k in selector
		]
	def helper(data):
		target = set()
		try:
			for sockets in matching(matching(matching(channels, role), session), language):
				target.update(sockets)
		except Exception as e:
			print(f"Failed compiling matching targets for role={role!r} session={session!r} language={language!r}\n{e!r}")
		websockets.broadcast(target, message_fn(data))
	return helper

for transcript in transcripts.values():
	transcript.subscribe("new", broadcast_update(
		lambda d: args(["new", "line", str(d)]),
		["reader", "editor"], default_session, transcript.language))
	transcript.subscribe("deleted", broadcast_update(
		lambda d: args(["deleted", "line", d.tid]),
		["reader", "editor"], default_session, transcript.language))
	transcript.subscribe("changed", broadcast_update(
		lambda d: args(["changed", "line", d.tid, "to", str(d)]),
		["reader", "editor"], default_session, transcript.language))
	transcript.subscribe("split", broadcast_update(
		lambda d: args(["split", "line", d[0].tid, "into", str(d[0]), "and", str(d[1])]),
		["reader", "editor"], default_session, transcript.language))
	transcript.subscribe("merged", broadcast_update(
		lambda d: args(["merged", "lines", d.tid, "as", str(d)]),
		["reader", "editor"], default_session, transcript.language))


class TCException(Exception):
	def __init__(self, websocket, msg=None):
		if msg is None:
			msg = "TCException"
		super(TCException, self).__init__(f"{msg} (from {websocket})")
		self.websocket = websocket

class EmptyCommandException(TCException):
	pass

class UnexpectedCommandException(TCException):
	def __init__(self, websocket, expected, actual):
		super(UnexpectedCommandException, self).__init__(websocket, f"Expected {str(expected)}, got {str(actual)}")

class UnexpectedKeywordException(TCException):
	def __init__(self, websocket, expected, actual, verbs):
		super(UnexpectedKeywordException, self).__init__(websocket, f"Expected {str(expected)}, got {str(actual)} in {verbs}")

class TooFewArgumentsException(TCException):
	def __init__(self, websocket, verbs):
		super(TooFewArgumentsException, self).__init__(websocket, f"Too few arguments for {str(verbs[0])}: {verbs[1:]}")

class UnknownCommandException(TCException):
	def __init__(self, websocket, cmd):
		super(UnknownCommandException, self).__init__(websocket, cmd)

class NonexistantChannelException(TCException):
	def __init__(self, websocket, channel):
		super(UnknownCommandException, self).__init__(websocket, f"Channel {str(channel)} doesn't exist")


editor_broadcast = broadcast_update(
	lambda d: args(["editor_broadcast", "from", d["sender"], d["msg"]]),
	["source", "editor"], default_session, language=None)

#websockets.broadcast(connected, "Hello!")

async def handler(websocket):
	logger.info("[%s] New connection", websocket.id)
	print(f"new connection")
	try:
		await websocket.send(args(["version", version.get("releaseTag", "Unknown")]))
		cmd = await expect("join", websocket)
		logger.info("[%s] cmd: %s", websocket.id, cmd)
		print(f"cmd: {cmd}")
		_, role, session, language = cmd["channel"].split("/")
		channel = (role, session, language)
		assert(role in channels)
		for s in sessions:
			if session == s.name or session == s.uuid:
				session = s
				break
		if type(session) is str:
			raise NonexistantChannelException(session)
		assert(language in session.transcripts)
		transcript = session.transcripts[language]
		if session not in channels[role]:
			channels[role][session] = dict()
		if language not in channels[role][session]:
			channels[role][session][language] = set()
		if len(channels[role][session][language]) == 0 and language in translators:
			translators[language].unpause()
			logger.info("[%s] unpausing translator for %s of %s", websocket.id, language, session)
			print(f"unpausing translator for {language} of {session}")
		await websocket.send(args(["confirm", cmd["counter"], cmd["channel"]]))

		connected.add(websocket)
		if role == "reader":
			await websocket.send(args(["existing", "transcript", f"[{', '.join(map(str, transcript.lines_sorted))}]"]))
			expected = ["leave"]
		elif role == "source":
			await websocket.send(args(["Authentication", "required"]))
			cmd = await expect(["auth"], websocket)
			expected = ["submit", "leave", "editor_broadcast"]
		elif role == "editor":
			await websocket.send(args(["Authentication", "required"]))
			cmd = await expect(["auth"], websocket)
			await websocket.send(args(["existing", "transcript", f"[{', '.join(map(str, transcript.lines_sorted))}]"]))
			expected = ["submit", "delete", "change", "split", "merge", "leave", "editor_broadcast"]
		channels[role][session][language].add(websocket)

		while True:
			cmd = await expect(expected, websocket)
			logger.info("[%s] cmd: %s", websocket.id, cmd)
			print(f"cmd: {cmd}")
			if cmd["cmd"] == "leave":
				if cmd["channel"] == f"/{channel}":
					await websocket.send(args(["Bye!"]))
					break
			elif cmd["cmd"] == "submit":
				lines = []
				for line in cmd["lines"]:
					line = Line.from_json(line)
					lines.append(transcript.add_line(line))
				await websocket.send(args(["confirm", cmd["counter"], f"[{', '.join(map(str, lines))}]"]))
			elif cmd["cmd"] == "delete":
				line = transcript.remove_line(cmd["tid"])
				await websocket.send(args(["confirm", cmd["counter"], str(line)]))
			elif cmd["cmd"] == "change":
				line = transcript.change_line(cmd["tid"], cmd["content"])
				await websocket.send(args(["confirm", cmd["counter"], str(line)]))
			elif cmd["cmd"] == "split":
				lines = transcript.split_line(cmd["tid"], int(cmd["position"]))
				await websocket.send(args(["confirm", cmd["counter"], f"[{', '.join(map(str, lines))}]"]))
			elif cmd["cmd"] == "merge":
				line = transcript.merge_lines(cmd["tid_one"], cmd["tid_two"])
				await websocket.send(args(["confirm", cmd["counter"], str(line)]))
			elif cmd["cmd"] == "editor_broadcast":
				editor_broadcast({
					"msg": cmd["msg"],
					"sender": websocket.id,
				})
				await websocket.send(args(["confirm", cmd["counter"]]))
			else:
				logger.info("[%s] Unhandled but expected command: %s", websocket.id, cmd)
				print(f"Unhandled but expected command: {cmd}")
	except (TCException, ValueError, AssertionError) as e:
		logger.error("[%s] Exception: %s", websocket.id, repr(e))
		print(repr(e))
		def sanitize(s):
			return s.split(" (from <websockets.")[0]
		await websocket.send(args([f"{e.__class__.__name__}({', '.join(map(sanitize, e.args))})"]))
	except (ConnectionClosedOK, ConnectionClosedError):
		logger.warning("[%s] Disconnected unexpectedly", websocket.id)
		print(f"disconnected unexpectedly {websocket}")
	finally:
		try:
			channels[role][session][language].remove(websocket)
			if len(channels[role][session][language]) == 0 and language in translators:
				translators[language].pause()
				logger.info("[%s] Pausing translator for %s of %s", websocket.id, language, session)
				print(f"pausing translator for {language} of {session}")
		except UnboundLocalError:
			pass
		if websocket in connected:
			connected.remove(websocket)
		logger.info("[%s] Handler stopped.", websocket.id)
		print(f"stopped {websocket}")


async def expect(cmds, websocket):
	if isinstance(cmds, str):
		cmds = [cmds]
	while True:
		msg = await websocket.recv()
		verbs = parse(msg)
		if verbs[0] == "ping":
			await websocket.send(args(["pong", SEP.join(verbs[1:])]))
		else:
			break
	if not len(verbs):
		raise EmptyCommandException(websocket)
	if verbs[0] not in cmds:
		raise UnexpectedCommandException(websocket, cmds, verbs[0])
	return parse_command(verbs)


def parse_command(verbs, websocket=None):
	if not verbs:
		raise EmptyCommandException(websocket)

	if verbs[0] == "ping":
		# ping <data>
		return {
			"cmd": "ping",
			"data": verbs[1:],
		}

	if verbs[0] == "join":
		# join <counter> <channel> id <id or None> [<client version>]
		if len(verbs) < 5:
			raise TooFewArgumentsException(websocket, verbs)
		if verbs[3] != "id":
			raise UnexpectedKeywordException(websocket, "id", verbs[3], verbs)
		return {
			"cmd": "join",
			"counter": verbs[1],
			"channel": verbs[2],
			"id": None if verbs[4] == "None" else verbs[4],
			"client_version": None if len(verbs) < 6 or verbs[5].lower() in ("none", "unknown") else verbs[5],
		}

	if verbs[0] == "leave":
		# leave <channel>
		if len(verbs) < 2:
			raise TooFewArgumentsException(websocket, verbs)
		return {
			"cmd": "leave",
			"channel": verbs[1],
		}

	if verbs[0] == "auth":
		# auth <secret>
		if len(verbs) < 2:
			raise TooFewArgumentsException(websocket, verbs)
		return {
			"cmd": "auth",
			"secret": verbs[1],
		}

	if verbs[0] == "new":
		# new <counter> session <name>
		if len(verbs) < 4:
			raise TooFewArgumentsException(websocket, verbs)
		return {
			"cmd": "new",
			"counter": verbs[1],
			"name": verbs[3],
		}

	if verbs[0] == "submit":
		# submit <counter> lines [<content> ]+
		if len(verbs) < 4:
			raise TooFewArgumentsException(websocket, verbs)
		if verbs[2] != "lines":
			raise UnexpectedKeywordException(websocket, "lines", verbs[2], verbs)
		return {
			"cmd": "submit",
			"counter": verbs[1],
			"lines": verbs[3:],
		}

	if verbs[0] == "delete":
		# delete <counter> line <tid>
		if len(verbs) < 4:
			raise TooFewArgumentsException(websocket, verbs)
		if verbs[2] != "line":
			raise UnexpectedKeywordException(websocket, "line", verbs[2], verbs)
		return {
			"cmd": "delete",
			"counter": verbs[1],
			"tid": verbs[3],
		}

	if verbs[0] == "change":
		# change <counter> line <tid> to <content>
		if len(verbs) < 6:
			raise TooFewArgumentsException(websocket, verbs)
		if verbs[2] != "line":
			raise UnexpectedKeywordException(websocket, "line", verbs[2], verbs)
		if verbs[4] != "to":
			raise UnexpectedKeywordException(websocket, "to", verbs[4], verbs)
		return {
			"cmd": "change",
			"counter": verbs[1],
			"tid": verbs[3],
			"content": verbs[5],
		}

	if verbs[0] == "split":
		# split <counter> line <tid> at <position>
		if len(verbs) < 6:
			raise TooFewArgumentsException(websocket, verbs)
		if verbs[2] != "line":
			raise UnexpectedKeywordException(websocket, "line", verbs[2], verbs)
		if verbs[4] != "at":
			raise UnexpectedKeywordException(websocket, "at", verbs[4], verbs)
		return {
			"cmd": "split",
			"counter": verbs[1],
			"tid": verbs[3],
			"position": verbs[5],
		}

	if verbs[0] == "merge":
		# merge <counter> lines <tid_one> and <tid_two>
		if len(verbs) < 6:
			raise TooFewArgumentsException(websocket, verbs)
		if verbs[2] != "lines":
			raise UnexpectedKeywordException(websocket, "lines", verbs[2], verbs)
		if verbs[4] != "and":
			raise UnexpectedKeywordException(websocket, "and", verbs[4], verbs)
		return {
			"cmd": "merge",
			"counter": verbs[1],
			"tid_one": verbs[3],
			"tid_two": verbs[5],
		}

	if verbs[0] == "editor_broadcast":
		# editor_broadcast <counter> <msg>
		if len(verbs) < 3:
			raise TooFewArgumentsException(websocket, verbs)
		return {
			"cmd": "editor_broadcast",
			"counter": verbs[1],
			"msg": verbs[2],
		}

	raise UnknownCommandException(verbs[0])


def parse(msg):
	remaining = msg
	verbs = []
	while remaining:
		if remaining.startswith(QUOTE) and QUOTE in remaining[1:]:
			try:
				endi = remaining.index(QUOTE, 1)
				verbs.append(remaining[1:endi])
				remaining = remaining[endi+1:].strip() # get rid of any additional whitespace
				continue
			except ValueError:
				pass
		try:
			i = remaining.index(SEP)
			s = remaining[0:i]
			verbs.append(s)
			remaining = remaining[i+1:].strip() # get rid of any additional whitespace
		except ValueError:
			verbs.append(remaining)
			break
	return verbs

def args(l):
	return SEP.join(map(lambda a: f"{QUOTE}{a}{QUOTE}" if not f"{a}".strip() or SEP in f"{a}" else f"{a}", l))



async def main():
	async with websockets.serve(handler, "0.0.0.0", 8765):
		logger.info("Server started: %s:%i", "0.0.0.0", 8765)
		print("server started")
		while True:
			await asyncio.gather(
				*map(lambda x: x.check_on_background_tasks(), translators.values()),
				asyncio.sleep(.01)
			)
		#await asyncio.Future()

if __name__ == "__main__":
	asyncio.run(main())
