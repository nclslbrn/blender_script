# blender_script

Creative coding with Python and Blender

### Mac OSX

To add new module

`cd /Applications/Blender.app/Contents/Resources/2.81/python`

`./bin/python/3.7m -m pip install <module_name>`

### Add custom module to python path

In .profile or .bash_profile (or if you use zsh shell in .zshrc) add
`export PYTHONPATH="$PYTHONPATH:/root/dir/subdir/this-repo-location/"`

You have to add the location of the repo into Blender Preferences / File Paths / Scripts
