import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, GObject


class Fruit(GObject.Object):
    name = GObject.Property(type=str)
    age = GObject.Property(type=int)
    cname = GObject.Property(type=str)

    def __init__(self, items):
        super().__init__()
        self.name = items[0]
        self.age = items[1]
        self.cname = items[2]


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(400, 400)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(self.box)

        # self.button_init()
        # self.listbox_init()
        # self.stack_init()
        # self.head_bar_init()
        # self.notebook_tabbed_layout()
        # self.text_style()
        # self.input_test()
        self.tree_init()

    def tree_init(self):
        # 创建一个列表模型
        fruits = [
            ["Banana", 1, "香蕉"],
            ["Apple", 2, "苹果"],
            ["Strawberry", 3, "草莓"],
            ["Pear", 4, "梨"],
        ]
        # 1 创建一个列表视图
        list_view = Gtk.ListView()
        # 2 store
        store = Gio.ListStore()

        for f in fruits:
            store.append(Fruit(f))

        ss = Gtk.SingleSelection()

        def on_selected_items_changed(selection, position, n_items):
            selected_item = selection.get_selected_item()
            if selected_item is not None:
                print(f"Selected item changed to: {selected_item.age}")

        ss.connect("selection-changed", on_selected_items_changed)
        ss.set_model(store)

        list_view.set_model(ss)
        # 3 创建一个列表项工厂
        factory = Gtk.SignalListItemFactory()

        def f_setup(fact, item):
            b = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            name_label = Gtk.Label(halign=Gtk.Align.CENTER)
            name_label.set_selectable(False)
            age_btn = Gtk.Label(halign=Gtk.Align.CENTER)
            cname_label = Gtk.Label(halign=Gtk.Align.CENTER)
            cname_label.set_selectable(False)
            b.append(name_label)
            b.append(age_btn)
            b.append(cname_label)

            item.set_child(b)

        factory.connect("setup", f_setup)

        def f_bind1(fact, item):
            fruit = item.get_item()
            child = item.get_child()
            fruit.bind_property(
                "name",
                child.get_first_child(),
                "label",
                GObject.BindingFlags.SYNC_CREATE,
            )
            fruit.bind_property(
                "age",
                child.get_last_child(),
                "label",
                GObject.BindingFlags.SYNC_CREATE,
            )
            fruit.bind_property(
                "cname",
                child.get_last_child(),
                "label",
                GObject.BindingFlags.SYNC_CREATE,
            )

        def f_bind(fact, item):
            item.get_child().set_label(item.get_item().name)

        factory.connect("bind", f_bind1)

        list_view.set_factory(factory)

        # 将TreeView添加到窗口中
        self.box.append(list_view)

    def input_test(self):
        self.user = Gtk.Entry(name="username", placeholder_text="请输入用户名")
        self.box.append(self.user)

        self.pwd = Gtk.Entry(name="passwd", placeholder_text="请输入密码")
        self.pwd.set_visibility(False)
        self.box.append(self.pwd)

        self.login = Gtk.Button(label="Login")
        self.login.connect("clicked", self.do_login)
        self.box.append(self.login)

    def do_login(self, button):
        print("login", self.user.get_text(), self.pwd.get_text())

    def text_style(self):
        self.box.set_homogeneous(False)
        # 左对齐
        vbox_l = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        vbox_l.set_homogeneous(False)

        l = Gtk.Label(label="plain left text label")
        vbox_l.append(l)
        l1 = Gtk.Label(
            label="asdfasdfasdfsd123123123123123lain left text label\n this is so cool text"
        )
        l1.set_justify(Gtk.Justification.LEFT)
        vbox_l.append(l1)
        # 右对齐
        vbox_r = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        vbox_r.set_homogeneous(False)
        r = Gtk.Label(label="plain right text label")
        vbox_r.append(r)
        r1 = Gtk.Label(
            label="asdfasdfasdfsd123123123123123lain right text label\n this is so cool text"
        )
        r1.set_justify(Gtk.Justification.RIGHT)
        vbox_r.append(r1)

        # 默认不换行
        r2 = Gtk.Label(label="asdfaight text label  this is so cool text")
        r2.set_wrap(True)
        vbox_r.append(r2)
        # fill newspaper
        r3 = Gtk.Label(
            label="asdfasasdfasdfasextasdfasdfasextasdfasdfasextasdfasdfasextasdfasdfasextasdfasdfasextdfasext label  this is so cool text"
        )
        r3.set_wrap(True)
        r3.set_justify(Gtk.Justification.FILL)
        vbox_r.append(r3)
        # Markup
        label = Gtk.Label()
        label.set_markup(
            "<small>small text</small>\n"
            "<big>small text</big>\n"
            "<b>small text</b>\n"
            "<a href='https://www.baidu.com'>small text</a>\n"
        )
        label.set_wrap(True)
        vbox_r.append(label)

        self.box.append(vbox_l)
        self.box.append(vbox_r)

    def notebook_tabbed_layout(self):
        note = Gtk.Notebook()
        self.set_child(note)

        page1 = Gtk.Box()
        page1.set_spacing(10)
        page1.append(Gtk.Label(label="Page 1"))
        page1_icon = Gtk.Image.new_from_icon_name("pan-end-symbolic")
        note.append_page(page1, page1_icon)
        page2 = Gtk.Box()
        page2.set_spacing(10)
        page2.append(Gtk.Label(label="Page 2"))
        page2_icon = Gtk.Image.new_from_icon_name("pan-end-symbolic")
        # note.append_page(page2, page2_icon)
        note.append_page(page2)

    def head_bar_init(self):
        headerbar = Gtk.HeaderBar(name="player")
        headerbar.set_show_title_buttons(True)

        # 图标名字从msys2\mingw64\share\icons\Adwaita\symbolic\ui获取
        # button
        audio_btn = Gtk.Button()
        cd_icon = Gio.ThemedIcon(name="checkbox-mixed-symbolic")
        image = Gtk.Image.new_from_gicon(cd_icon)
        audio_btn.set_child(image)

        headerbar.pack_end(audio_btn)
        # link
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        # box.get_style_context().add_class("linked")
        style_context = box.get_style_context()
        style_context.add_class("linked")
        # provider = Gtk.CssProvider()
        # provider.load_from_data(
        #     b"""
        # .linked {
        #     background-color: red;
        #     border: 1px solid #ddd;
        #     border-radius: 4px;
        # }
        # """
        # )
        # Gtk.StyleContext.add_provider_for_display(
        #     Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        # )

        # left arrow
        la = Gtk.Button()
        image = Gtk.Image.new_from_icon_name("pan-start-symbolic")
        la.set_child(image)
        box.append(la)
        ra = Gtk.Button()
        image = Gtk.Image.new_from_icon_name("pan-end-symbolic")
        ra.set_child(image)
        box.append(ra)

        headerbar.pack_start(box)

        self.set_titlebar(headerbar)
        self.set_child(Gtk.TextView())

    def stack_init(self):
        arae = Gtk.Stack()
        arae.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        arae.set_transition_duration(1000)

        c = Gtk.CheckButton(label="mmmm")
        arae.add_titled(c, "check name ", "check box")
        l = Gtk.Label(label="这是一个label")
        l.set_markup("<big>huge</big")
        arae.add_titled(l, "label name", "label big")
        s = Gtk.StackSwitcher()
        s.set_stack(arae)

        self.box.append(s)
        self.box.append(arae)

    def listbox_init(self):
        # row1
        row_1 = Gtk.ListBoxRow()
        box_1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row_1.set_child(box_1)

        label1 = Gtk.Label(label="Label")
        checkbox1 = Gtk.CheckButton()
        box_1.append(label1)
        box_1.append(checkbox1)

        self.box.append(row_1)
        # row2
        row_2 = Gtk.ListBoxRow()
        box_2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row_2.set_child(box_2)

        label2 = Gtk.Label(label="第二个")
        switch1 = Gtk.Switch()
        box_2.append(label2)
        box_2.append(switch1)

        self.box.append(row_2)

    def button_init(self):
        button = Gtk.Button(label="Hello")
        self.box.append(button)
        button.connect("clicked", self.hello)

    def hello(self, button):
        print("Hello world")


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.win = None
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.set_title("测试工具")
        self.win.present()


app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
