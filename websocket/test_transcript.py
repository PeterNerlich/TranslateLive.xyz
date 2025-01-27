import json
import uuid
from datetime import datetime, timedelta

from transcript import Line, Transcript


def test_export_srt():
	start = datetime(year=2025, month=2, day=7, hour=8)

	transcript = Transcript("de", time_offset=start.timestamp())
	transcript.add_line(start=(start+timedelta(seconds=1.0000)).timestamp(), end=(start+timedelta(seconds=3.2383)).timestamp(), text="line a")
	transcript.add_line(start=(start+timedelta(seconds=3.2383)).timestamp(), end=(start+timedelta(seconds=4.5000)).timestamp(), text="line b")
	transcript.add_line(start=(start+timedelta(seconds=5.0003)).timestamp(), end=(start+timedelta(seconds=9.1234)).timestamp(), text="line c")

	assert transcript.to_srt() == """1
00:00:01,000 --> 00:00:03,238
line a

2
00:00:03,238 --> 00:00:04,500
line b

3
00:00:05,000 --> 00:00:09,123
line c

"""
