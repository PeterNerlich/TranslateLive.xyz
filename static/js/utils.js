
class UUIDv4 extends String {
	constructor() {
		const id = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
			const r = Math.random() * 16 | 0, 
				v = c == 'x' ? r : (r & 0x3 | 0x8);
			return v.toString(16);
		});
		super(id);
	}
}


/**************************************/

const uLetters = 'A-Za-z\u00AA\u00B5\u00BA\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02C1\u02C6-\u02D1\u02E0-\u02E4\u02EC\u02EE\u0370-\u0374\u0376\u0377\u037A-\u037D\u037F\u0386\u0388-\u038A\u038C\u038E-\u03A1\u03A3-\u03F5\u03F7-\u0481\u048A-\u052F\u0531-\u0556\u0559\u0561-\u0587\u05D0-\u05EA\u05F0-\u05F2\u0620-\u064A\u066E\u066F\u0671-\u06D3\u06D5\u06E5\u06E6\u06EE\u06EF\u06FA-\u06FC\u06FF\u0710\u0712-\u072F\u074D-\u07A5\u07B1\u07CA-\u07EA\u07F4\u07F5\u07FA\u0800-\u0815\u081A\u0824\u0828\u0840-\u0858\u08A0-\u08B4\u0904-\u0939\u093D\u0950\u0958-\u0961\u0971-\u0980\u0985-\u098C\u098F\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BD\u09CE\u09DC\u09DD\u09DF-\u09E1\u09F0\u09F1\u0A05-\u0A0A\u0A0F\u0A10\u0A13-\u0A28\u0A2A-\u0A30\u0A32\u0A33\u0A35\u0A36\u0A38\u0A39\u0A59-\u0A5C\u0A5E\u0A72-\u0A74\u0A85-\u0A8D\u0A8F-\u0A91\u0A93-\u0AA8\u0AAA-\u0AB0\u0AB2\u0AB3\u0AB5-\u0AB9\u0ABD\u0AD0\u0AE0\u0AE1\u0AF9\u0B05-\u0B0C\u0B0F\u0B10\u0B13-\u0B28\u0B2A-\u0B30\u0B32\u0B33\u0B35-\u0B39\u0B3D\u0B5C\u0B5D\u0B5F-\u0B61\u0B71\u0B83\u0B85-\u0B8A\u0B8E-\u0B90\u0B92-\u0B95\u0B99\u0B9A\u0B9C\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8-\u0BAA\u0BAE-\u0BB9\u0BD0\u0C05-\u0C0C\u0C0E-\u0C10\u0C12-\u0C28\u0C2A-\u0C39\u0C3D\u0C58-\u0C5A\u0C60\u0C61\u0C85-\u0C8C\u0C8E-\u0C90\u0C92-\u0CA8\u0CAA-\u0CB3\u0CB5-\u0CB9\u0CBD\u0CDE\u0CE0\u0CE1\u0CF1\u0CF2\u0D05-\u0D0C\u0D0E-\u0D10\u0D12-\u0D3A\u0D3D\u0D4E\u0D5F-\u0D61\u0D7A-\u0D7F\u0D85-\u0D96\u0D9A-\u0DB1\u0DB3-\u0DBB\u0DBD\u0DC0-\u0DC6\u0E01-\u0E30\u0E32\u0E33\u0E40-\u0E46\u0E81\u0E82\u0E84\u0E87\u0E88\u0E8A\u0E8D\u0E94-\u0E97\u0E99-\u0E9F\u0EA1-\u0EA3\u0EA5\u0EA7\u0EAA\u0EAB\u0EAD-\u0EB0\u0EB2\u0EB3\u0EBD\u0EC0-\u0EC4\u0EC6\u0EDC-\u0EDF\u0F00\u0F40-\u0F47\u0F49-\u0F6C\u0F88-\u0F8C\u1000-\u102A\u103F\u1050-\u1055\u105A-\u105D\u1061\u1065\u1066\u106E-\u1070\u1075-\u1081\u108E\u10A0-\u10C5\u10C7\u10CD\u10D0-\u10FA\u10FC-\u1248\u124A-\u124D\u1250-\u1256\u1258\u125A-\u125D\u1260-\u1288\u128A-\u128D\u1290-\u12B0\u12B2-\u12B5\u12B8-\u12BE\u12C0\u12C2-\u12C5\u12C8-\u12D6\u12D8-\u1310\u1312-\u1315\u1318-\u135A\u1380-\u138F\u13A0-\u13F5\u13F8-\u13FD\u1401-\u166C\u166F-\u167F\u1681-\u169A\u16A0-\u16EA\u16F1-\u16F8\u1700-\u170C\u170E-\u1711\u1720-\u1731\u1740-\u1751\u1760-\u176C\u176E-\u1770\u1780-\u17B3\u17D7\u17DC\u1820-\u1877\u1880-\u18A8\u18AA\u18B0-\u18F5\u1900-\u191E\u1950-\u196D\u1970-\u1974\u1980-\u19AB\u19B0-\u19C9\u1A00-\u1A16\u1A20-\u1A54\u1AA7\u1B05-\u1B33\u1B45-\u1B4B\u1B83-\u1BA0\u1BAE\u1BAF\u1BBA-\u1BE5\u1C00-\u1C23\u1C4D-\u1C4F\u1C5A-\u1C7D\u1CE9-\u1CEC\u1CEE-\u1CF1\u1CF5\u1CF6\u1D00-\u1DBF\u1E00-\u1F15\u1F18-\u1F1D\u1F20-\u1F45\u1F48-\u1F4D\u1F50-\u1F57\u1F59\u1F5B\u1F5D\u1F5F-\u1F7D\u1F80-\u1FB4\u1FB6-\u1FBC\u1FBE\u1FC2-\u1FC4\u1FC6-\u1FCC\u1FD0-\u1FD3\u1FD6-\u1FDB\u1FE0-\u1FEC\u1FF2-\u1FF4\u1FF6-\u1FFC\u2071\u207F\u2090-\u209C\u2102\u2107\u210A-\u2113\u2115\u2119-\u211D\u2124\u2126\u2128\u212A-\u212D\u212F-\u2139\u213C-\u213F\u2145-\u2149\u214E\u2183\u2184\u2C00-\u2C2E\u2C30-\u2C5E\u2C60-\u2CE4\u2CEB-\u2CEE\u2CF2\u2CF3\u2D00-\u2D25\u2D27\u2D2D\u2D30-\u2D67\u2D6F\u2D80-\u2D96\u2DA0-\u2DA6\u2DA8-\u2DAE\u2DB0-\u2DB6\u2DB8-\u2DBE\u2DC0-\u2DC6\u2DC8-\u2DCE\u2DD0-\u2DD6\u2DD8-\u2DDE\u2E2F\u3005\u3006\u3031-\u3035\u303B\u303C\u3041-\u3096\u309D-\u309F\u30A1-\u30FA\u30FC-\u30FF\u3105-\u312D\u3131-\u318E\u31A0-\u31BA\u31F0-\u31FF\u3400-\u4DB5\u4E00-\u9FD5\uA000-\uA48C\uA4D0-\uA4FD\uA500-\uA60C\uA610-\uA61F\uA62A\uA62B\uA640-\uA66E\uA67F-\uA69D\uA6A0-\uA6E5\uA717-\uA71F\uA722-\uA788\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA801\uA803-\uA805\uA807-\uA80A\uA80C-\uA822\uA840-\uA873\uA882-\uA8B3\uA8F2-\uA8F7\uA8FB\uA8FD\uA90A-\uA925\uA930-\uA946\uA960-\uA97C\uA984-\uA9B2\uA9CF\uA9E0-\uA9E4\uA9E6-\uA9EF\uA9FA-\uA9FE\uAA00-\uAA28\uAA40-\uAA42\uAA44-\uAA4B\uAA60-\uAA76\uAA7A\uAA7E-\uAAAF\uAAB1\uAAB5\uAAB6\uAAB9-\uAABD\uAAC0\uAAC2\uAADB-\uAADD\uAAE0-\uAAEA\uAAF2-\uAAF4\uAB01-\uAB06\uAB09-\uAB0E\uAB11-\uAB16\uAB20-\uAB26\uAB28-\uAB2E\uAB30-\uAB5A\uAB5C-\uAB65\uAB70-\uABE2\uAC00-\uD7A3\uD7B0-\uD7C6\uD7CB-\uD7FB\uF900-\uFA6D\uFA70-\uFAD9\uFB00-\uFB06\uFB13-\uFB17\uFB1D\uFB1F-\uFB28\uFB2A-\uFB36\uFB38-\uFB3C\uFB3E\uFB40\uFB41\uFB43\uFB44\uFB46-\uFBB1\uFBD3-\uFD3D\uFD50-\uFD8F\uFD92-\uFDC7\uFDF0-\uFDFB\uFE70-\uFE74\uFE76-\uFEFC\uFF21-\uFF3A\uFF41-\uFF5A\uFF66-\uFFBE\uFFC2-\uFFC7\uFFCA-\uFFCF\uFFD2-\uFFD7\uFFDA-\uFFDC';
const uDigits = '0-9\u0660-\u0669\u06F0-\u06F9\u07C0-\u07C9\u0966-\u096F\u09E6-\u09EF\u0A66-\u0A6F\u0AE6-\u0AEF\u0B66-\u0B6F\u0BE6-\u0BEF\u0C66-\u0C6F\u0CE6-\u0CEF\u0D66-\u0D6F\u0DE6-\u0DEF\u0E50-\u0E59\u0ED0-\u0ED9\u0F20-\u0F29\u1040-\u1049\u1090-\u1099\u17E0-\u17E9\u1810-\u1819\u1946-\u194F\u19D0-\u19D9\u1A80-\u1A89\u1A90-\u1A99\u1B50-\u1B59\u1BB0-\u1BB9\u1C40-\u1C49\u1C50-\u1C59\uA620-\uA629\uA8D0-\uA8D9\uA900-\uA909\uA9D0-\uA9D9\uA9F0-\uA9F9\uAA50-\uAA59\uABF0-\uABF9\uFF10-\uFF19';
const uPunctuation = '!-#%-*,-/\:;?@\[-\]_\{\}\u00A1\u00A7\u00AB\u00B6\u00B7\u00BB\u00BF\u037E\u0387\u055A-\u055F\u0589\u058A\u05BE\u05C0\u05C3\u05C6\u05F3\u05F4\u0609\u060A\u060C\u060D\u061B\u061E\u061F\u066A-\u066D\u06D4\u0700-\u070D\u07F7-\u07F9\u0830-\u083E\u085E\u0964\u0965\u0970\u0AF0\u0DF4\u0E4F\u0E5A\u0E5B\u0F04-\u0F12\u0F14\u0F3A-\u0F3D\u0F85\u0FD0-\u0FD4\u0FD9\u0FDA\u104A-\u104F\u10FB\u1360-\u1368\u1400\u166D\u166E\u169B\u169C\u16EB-\u16ED\u1735\u1736\u17D4-\u17D6\u17D8-\u17DA\u1800-\u180A\u1944\u1945\u1A1E\u1A1F\u1AA0-\u1AA6\u1AA8-\u1AAD\u1B5A-\u1B60\u1BFC-\u1BFF\u1C3B-\u1C3F\u1C7E\u1C7F\u1CC0-\u1CC7\u1CD3\u2010-\u2027\u2030-\u2043\u2045-\u2051\u2053-\u205E\u207D\u207E\u208D\u208E\u2308-\u230B\u2329\u232A\u2768-\u2775\u27C5\u27C6\u27E6-\u27EF\u2983-\u2998\u29D8-\u29DB\u29FC\u29FD\u2CF9-\u2CFC\u2CFE\u2CFF\u2D70\u2E00-\u2E2E\u2E30-\u2E42\u3001-\u3003\u3008-\u3011\u3014-\u301F\u3030\u303D\u30A0\u30FB\uA4FE\uA4FF\uA60D-\uA60F\uA673\uA67E\uA6F2-\uA6F7\uA874-\uA877\uA8CE\uA8CF\uA8F8-\uA8FA\uA8FC\uA92E\uA92F\uA95F\uA9C1-\uA9CD\uA9DE\uA9DF\uAA5C-\uAA5F\uAADE\uAADF\uAAF0\uAAF1\uABEB\uFD3E\uFD3F\uFE10-\uFE19\uFE30-\uFE52\uFE54-\uFE61\uFE63\uFE68\uFE6A\uFE6B\uFF01-\uFF03\uFF05-\uFF0A\uFF0C-\uFF0F\uFF1A\uFF1B\uFF1F\uFF20\uFF3B-\uFF3D\uFF3F\uFF5B\uFF5D\uFF5F-\uFF65';

const wordReg = new RegExp(
	`(\n+|\t+| +|[${uLetters}]+|[${uDigits}]+|[^${uLetters}${uDigits}\n\t ]+)`
, "g")

function splitwords(s) {
	return s.match(wordReg) || [];
}

function wordDiff(a, b) {
	return new Diff(splitwords(a), splitwords(b));
}


/**************************************/


function logAll(obj, name, except, predicate) {
	for (let key in obj.eventListeners) {
		// Don't register listener for exempted events
		if (except && except.includes(key)) continue;
		obj.subscribe(key, msg => {
			// Only log events for which a special condition is true
			if (predicate && !predicate(key, msg)) return;
			console.log.bind(this, `[${name} | ${key}]`);
		});
	}
}


/**************************************/


const getClientVersion = (() => {
	let promise;

	return url => {
		if (promise === undefined) {
			promise = fetch(url || "version.json").then(response => {
				if (!response.ok) {
					throw new Error("HTTP error " + response.status);
				}
				return response.json();
			}).then(json => {
				return json.releaseTag;
			}).catch(error => {
				version = null;
				throw error;
			});
		}
		return promise;
	}
})();

function displayClientVersion() {
	const versionDiv = document.getElementById("version");
	const clientVersionDiv = versionDiv ? versionDiv.querySelector("#client") : null;
	const fallback = "version.json";
	const url = clientVersionDiv ? clientVersionDiv.getAttribute("data-src") || fallback : fallback;
	if (clientVersionDiv) {
		return getClientVersion(url).then(version => {
			clientVersionDiv.innerText = `Version: ${version}`;
		}).catch(e => {
			clientVersionDiv.innerText = "Version: Unknown";
		});
	}
}

function displayServerVersion(version) {
	const versionDiv = document.getElementById("version");
	const serverVersionDiv = versionDiv ? versionDiv.querySelector("#server") : null;
	if (serverVersionDiv) {
		serverVersionDiv.innerText = `| Server: ${version}`;
	}
}


/**************************************/


function parseQueryArgs(query) {
	const fields = query.slice(1).split("&");
	let out = {}
	for (const arg of fields) {
		const key = arg.split("=")[0];
		const value = arg.slice(key.length+1);
		out[key] = value;
	}
	return out;
}


/**************************************/


function setupStickyScroll(elem, clearance, debug) {
	let shouldScroll;
	if (clearance === undefined) clearance = (target) => target.clientHeight * 0.2;
	else if (typeof clearance !== "function") clearance = (target) => clearance;
	if (debug) console.log(`setupStickyScroll(${elem}, ${clearance}, ${debug}) elem=${elem}`);

	function calculateShouldScroll() {
		shouldScroll = elem.scrollTop + elem.clientHeight + clearance(elem) >= elem.scrollHeight;
		if (debug) console.log(`calculateShouldScroll() shouldScroll=${shouldScroll} (scrollTop ${elem.scrollTop} + clientHeight ${elem.clientHeight} + ${clearance(elem)} >= scrollHeight ${elem.scrollHeight}, for ${elem})`);
		return shouldScroll;
	}
	function scrollToBottom(force) {
	    if (debug) console.log(`scrollToBottom(${force}) shouldScroll=${shouldScroll} (${elem})`);
  		if (shouldScroll || force) {
			elem.scrollTop = elem.scrollHeight;
		}
	}
	window.addEventListener("scroll", calculateShouldScroll);
	window.addEventListener("resize", scrollToBottom);

	return {calculateShouldScroll, scrollToBottom};
}


/**************************************/


const hasCSSPow = (debug => {
	const start = Date.now();
	// test whether pow() exists in CSS or just results in empty value
	const div = document.createElement("div");
	div.style.setProperty("opacity", "pow(0.5, 2)");
	document.body.appendChild(div);
	const opacity = getComputedStyle(div).getPropertyValue("opacity");
	const hasPow = opacity == "0.25";
	div.remove();
	const end = Date.now();
	if (debug) console.log(`[hasCSSPow] ${hasPow} (opacity is ${JSON.stringify(opacity)}, check took ${(end-start)/1000} s)`);
	return hasPow;
})(true);


/**************************************/


function debounce(func, wait, immediate) {
	let timeout;
	return function() {
		const context = this,
			args = arguments;
		const callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(function() {
			timeout = null;
			if (!immediate) {
				func.apply(context, args);
			}
		}, wait);
		if (callNow) func.apply(context, args);
	}
}

function stateDebounce(func, wait, immediate, debug) {
	if (debug) console.log(`[debounce] stateDebounce(${func}, ${JSON.stringify(wait)}, ${JSON.stringify(immediate)}, ${JSON.stringify(debug)})`);

	if (immediate) {
		const lastStates = [];
		if (debug) console.log(`[debounce] lastStates = ${JSON.stringify(lastStates)}`);
		return function(state) {
			if (debug) console.log(`[debounce] new state ${JSON.stringify(state)} (in lastStates: ${lastStates.includes(state)})`);
			const context = this,
				args = arguments;
			if (!lastStates.includes(state)) {
				func.apply(context, args);
			}
			lastStates.push(state);
			setTimeout(() => {
				if (lastStates.length > 1) {
					// leave at least one element in
					lastStates.splice(0,1);
				}
			}, wait);
			if (debug) console.log(`[debounce] set lastStates = ${JSON.stringify(lastStates)}`);
		}

	} else {
		let activeState,
			targetState;
		let timeout = null;
		return function(state) {
			const context = this,
				args = arguments;
			if (timeout === null || state !== targetState) {
				timeout = setTimeout(() => {
					if (state !== activeState && state === targetState) {
						activeState = state;
						func.apply(context, args);
					}
				}, wait);
				targetState = state;
			}
		}
	}
}

/****************************/

function exponentialBackoff(start=1, max=null, scalar=2) {
	if (start <= 0) throw Error("Start for exponential backoff cannot be 0 or negative");
	let iterations = 0;
	let lastCall = null;
	return (reset=false) => {
		const now = Date.now();
		const call = lastCall === null ?
			"first call" :
			`last call ${now - lastCall} ms ago`;
		lastCall = now;
		const value = Math.pow(scalar, iterations++) * start;
		console.log(`expBo value = ${value} = ${scalar}^${iterations} * ${start} (${call})`);
		if (reset) {
			console.log("  resetting iterations = 0");
			iterations = 0;
		}
		if (max == null) return value;
		return Math.min(max, value);
	};
}

/****************************/

if (Set.prototype.union === undefined) {
	Set.prototype.union = function union(setB) {
		const _union = new Set(this);
		for (const elem of setB) {
			_union.add(elem);
		}
		return _union;
	}
}

const isFunction = function(obj) {
  return !!(obj && obj.constructor && obj.call && obj.apply);
};
window.IsCallable = typeof IsCallable === "undefined" ? isFunction : IsCallable;

if (Array.prototype.toSorted === undefined) {
	Array.prototype.toSorted = function toSorted(comparefn) {
		if (typeof comparefn !== 'undefined' && !IsCallable(comparefn))
			throw new $TypeError('`comparefn` must be a function');
		var a = Array.from(this);
		a.sort(comparefn);
		return a;
	}
}
