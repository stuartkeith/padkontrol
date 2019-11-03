# padkontrol

padkontrol is a Python module used to interact with the Korg PadKontrol MIDI controller via its native mode.


## Installation

You can install the module via pip:

```shell
pip install "git+https://github.com/stuartkeith/padkontrol.git"
```

Then import and use:

```python
import padkontrol
```

See `example.py` for usage.

The example uses [python-rtmidi](http://trac.chrisarndt.de/code/wiki/python-rtmidi) for MIDI IO.
You might need to modify the OUTPUT_MIDI_PORT and INPUT_MIDI_PORT variables.


## Acknowledgements

Thanks to h2a2p for writing the "Guide to PadKontrol Native Mode - Version 2.1" PDF (downloaded from [http://www.korgforums.com/forum/phpBB2/viewtopic.php?t=28030](http://www.korgforums.com/forum/phpBB2/viewtopic.php?t=28030)).
