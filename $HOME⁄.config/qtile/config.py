from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os

mod = "mod4"
terminal = guess_terminal()

# Keybindings
keys = [
    # Movimiento entre ventanas
    *[
        Key([mod], k, f())
        for k, f in zip("hjkl", [lazy.layout.left, lazy.layout.down, lazy.layout.up, lazy.layout.right])
    ],
    Key([mod], "space", lazy.layout.next()),

    # Mover ventanas
    *[
        Key([mod, "shift"], k, f())
        for k, f in zip("hjkl", [lazy.layout.shuffle_left, lazy.layout.shuffle_down, lazy.layout.shuffle_up, lazy.layout.shuffle_right])
    ],

    # Redimensionar ventanas
    *[
        Key([mod, "control"], k, f())
        for k, f in zip("hjkl", [lazy.layout.grow_left, lazy.layout.grow_down, lazy.layout.grow_up, lazy.layout.grow_right])
    ],
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "Tab", lazy.next_layout()),

    # Administración de ventanas
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),

    # Configuración
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
   
    # Abrir Dolphin
    Key([mod], "e", lazy.spawn("dolphin")), 
   
    # Lanzador
    Key(
        [mod], "r",
        lazy.spawn("bash /home/enzo/rofi/files/launchers/type-4/launcher.sh")
    ),
]

# Grupos
groups = [Group(str(i), label="●") for i in range(1, 7)]

for group in groups:
    keys.extend([
        Key([mod], group.name, lazy.group[group.name].toscreen()),
        Key([mod, "shift"], group.name, lazy.window.togroup(group.name, switch_group=True)),
    ])

# Layouts
layouts = [
    layout.Columns(
        border_focus="#7b5cb5",
        border_normal="#7b5cb5",
        border_focus_stack=["#d75f5f", "#8f3d3d"],
        border_width=0,
        margin=6,
        ratio=0.5,
    ),
    layout.Max(),
]

# Widgets
widget_defaults = dict(
    font="Fira Code Nerd Font",
    fontsize=13,
    padding=4,
)
extension_defaults = widget_defaults.copy()

# Screens
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method="text",
                    rounded=True,
                    inactive="#666666",
                    active="#a19fe3",
                    this_current_screen_border="#8381cc",
                    urgent_border="#FF00FF",
                    fontsize=26,
                    margin_x=1,
                    padding=1,
                    disable_drag=True,
                ),

                widget.Spacer(length=10),

                widget.Prompt(),

                widget.Spacer(length=bar.STRETCH),

                widget.Systray(
                    padding=5,
                ),

                widget.TextBox(
                    text="",
                    fontsize=28,
                    padding=-1,
                    foreground="#4a5682",
                    background="#1f2129",
                ),

                widget.CheckUpdates(
                    distro="Arch",
                    update_interval=1800,
                    no_update_string="",
                    display_format=" {updates}",
                    foreground="#b3c4fc",
                    background="#4a5682",
                    colour_have_updates="#e3ebfa",
                    colour_no_updates="#e3ebfa",
                    mouse_callbacks={
                        'Button1': lazy.spawn("alacritty -e sudo pacman -Syu"),
                    },
                ),

                widget.TextBox(
                    text="",
                    fontsize=28,
                    padding=-1,
                    foreground="#556180",
                    background="#4a5682",
                ),

                widget.Clock(
                    format=" %d/%m/%Y - %H:%M",
                    foreground="#e3ebfa",
                    background="#556180",
                ),

                widget.TextBox(
                    text="",
                    fontsize=28,
                    padding=0,
                    foreground="#ffffff",
                    background="#556180",
                ),

                widget.TextBox(
                    text="  ",
                    fontsize=20,
                    background="#ffffff",
                    foreground="#586af5",
                    padding=-1,
                ),
            ],
            32,
            margin=[4, 5, 2, 5],
            background="#1f2129",
            opacity=7,
        ),
    ),
]

# Mouse
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# Floating Layout
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ],
    border_focus="#655ec4",
    border_normal="#7b5cb5",
    border_width=0,
)

# Qtile Settings
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "LG3D"

# Autostart
@hook.subscribe.startup_once
def autostart():
    apps = [
        "picom",
        "nitrogen --restore",
    ]
    for app in apps:
        os.system(f"{app} &")
