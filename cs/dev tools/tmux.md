- program that runs inside a [[terminal]] and can run other terminal programs inside it

Each program inside tmux gets its **own** terminal managed by tmux and can be acessed from the single terminal where tmux is running.

This is called [[multiplexing]] a tmux is a [[terminal multiplexer]].

Programs that run inside tmux may be 
- full screen interactive programs like [[nvim]] or top 
- shells like [[bash]] or ksh
- or any other program that can be run in a [[Unix]] terminal

There is a powerful feature set to **access**, **manage** and **organize** programs inside tmux.

Main uses of tmux:
- Protect running programs on a remote server from connection drops 
- Allows work with multiple programs and shells together in one terminal a bit like a [[window manager]]

## How I am currently using it
I am using [[i3wm]] + [[neovim]]. I recently wanted to explore this keyboard-less setup even more and read something about tmux. 
I am currently using from school and my own projects. It can be quite usefuil, I was heavily inspired by these articles:
https://www.bugsnag.com/blog/tmux-and-vim/
https://thoughtbot.com/blog/a-tmux-crash-course


Here is a cheatsheet
https://tmuxcheatsheet.com/
## Basic concepts
- these concepts are important to be familiar with

### tmux [[server]] and [[clients]]
tmux keeps all its state in a single main [[process]], called tmux server. 

This runs in the background and manages all the programs running inside tmux and keeps track of their output.

Tmux server is started **automatically** when user runs a `tmux` command and by default exits when there are no running programs.

Users attch to the tmux server by starting a client. This client takes over the terminal and communicates with server using socket file in `/tmp`.

### Sessions, windows and panes

#### Session
 - A tmux session is a collection of windows. Basically a workspace. Each session can have multiple windows and panes, you can detach from and reattach to a session.
 
###### Technical perspective
- session is a collection of terminal instances that remain active in the background, maintaing ther processes, [[I/O streams]] and state, even if the user detaches or terminates the terminal window. Internally, sessions allow multiplexing of terminal I/O through a single interface.

#### Windows
- A window in tmux is similar to a tab in terminal emulator. Each session can have mutliple windows that can be switched. Each window can contain a full-screen terminal or be split into multiple panes.
###### Technical perspective
A winows a basically a virtual terminal within a session. It is implemented as a seperate process and each window can have multiple panes that share resources like input and output buffers. The window [[multiplexes access|multiplex]] to the terminal process running in it. This isolates it from other windows but keep it a part of the session process.

#### Pane
- Pane is a subdivision of a window. You can split window into multiple panes (horizontally or vertically).
- Each pane acts like a **independent [[terminal]]**
###### Technical perspective
Each pane has its own terminal I/O buffer and can independently run its own commands. The splitting of panes is handled by dynamically ajusting the terminal size and reallocating resource accordingly. This allows simultaneous display of multiple command streams withn a single terminal.

#### The status line
When a tmux client is attached, it shows a status line on the bottom line of the screen.
![[Pasted image 20240912183645.png]]

#### Detach
- Detaching a session allows you to leave it running in the background and return to it later - programs in the session will keep running even if you close the [[terminal]] window.
###### Technical perspective
Detaching from a session involves removing the terminal's interactive interface while maintaining the session's process tree in [[memory]]. The session continues to run, with no user I/O stream attached to it, yet its processes and system resources remain unaffected. Detaching essentially severs the terminal from the session, but the session remains as a background [[daemon]].

#### Attach
- Attaching a session means reconnectiong to a previously detached session. You can reattach using `tmux attach` command.
###### Technical perspective
Attaching involves re-binding the terminal's I/O [[file descriptors]] to the session, restoring full interactivity. The session's [[virtual terminal|terminal#virtual terminal]] devices ([[PTYs]]) are reconnected to the [[physical terminal|terminal]], allowing the user to resume interacting with the precesses that were running in the background.

#### Prefix key
- prefix key is a key combination that you press to issue a tmux commands. By default it is `ctrl + b`. After pressing the prefix key you can follow it with another key to execute command (e.g. `ctrl-b c` to create a new window)

#### Layout
- Layouts in tmux control how the panes are arranged withing a window. You can cycle throught different layouts (e.g. even horizontal, even vertical, tiled) to organize your panes in the most useful way.
- Example: You might use a tiled layout when you want all panes to be visible in equal portions

#### Command mode
- In command mode you can type more complex tmux commands. Enter command mode by presing the [[tmux#Prefix key]] followed by `:`. Then you can type a command like `new-session` or `split-window`

## tmux.conf
This is a file where you can customize tmuix's behavior by setting keybindings, cahnging options and defining aliases for commands. File is typically located in your home dir (`~/.tmux.conf`)

- `tmux.conf` is a plaintext configuration file that tmux parses upon initialization. It contains directives written in a domain-specific configuration language. 

## Buffer
tmux uses buffers to store text that you have copied within a session. This is simall to a clipboard, allowing you to copy and paste between panes or windows.

## Scrollback
Scrollback buffer refers to a history of output in a pane that you can scroll through. It allows you to view past command and output that have scrolled off the screen.
- you can enter scrollback mode using [[tmux#Prefix key]] + `[` and navigate through the pane's output

## Plugins
There is a lot of community pluging you can find. All use a tool named [[TPM]] (Tmux Plugin Manager).

I am using it to store sessions even after PC has been shut down.