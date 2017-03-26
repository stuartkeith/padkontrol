# padkontrol
Version 1.0

By Stuart Keith

padkontrol is a Python module used to interact with the Korg PadKontrol MIDI controller via its native mode.

# How to use
First install the module
```shell
pip install "git+https://github.com/stuartkeith/padkontrol.git"
```

Now simply import the module and you're all set
```python
import padkontrol
```

See `example.py` for more in-depth usage.
The example uses [python-rtmidi](http://trac.chrisarndt.de/code/wiki/python-rtmidi) for MIDI IO.
You will probably have to modify the OUTPUT_MIDI_PORT and INPUT_MIDI_PORT variables.

# Acknowledgements
Thanks to h2a2p for writing the "Guide to PadKontrol Native Mode - Version 2.1" PDF (downloaded from [http://www.korgforums.com/forum/phpBB2/viewtopic.php?t=28030](http://www.korgforums.com/forum/phpBB2/viewtopic.php?t=28030)).
