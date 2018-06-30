import tkinter as tk
import tkinter.ttk as ttk
import LanguageDeck.ui.maps as maps
import LanguageDeck.ui.decks as deck_ui
from LanguageDeck.models import Cards, decks
from LanguageDeck.session_tools.session_scope import session_scope


class CardView(ttk.Frame):
    def __init__(self, card, master=None, session_factory=None, root=None, descendants=()):
        super().__init__(master, padding=5)
        # tree relationships
        self.root = root if root else self
        self.descendants = descendants
        self.card = card

        # card data
        self.card_id = card.id
        self.card_type = type(card)
        self.card_text = card.text
        if type(card) == Cards.LanguageAVocab or type(card) == Cards.LanguageBVocab:
            self.examples = [{k: v for (k, v) in zip(('id','text', 'type'),
                                                     (c.id, c.text, type(c)))} for c in card.examples]
        else:
            self.examples = [{k: v for (k, v) in zip(('id','text', 'type'),
                                                     (c.id, c.text, type(c)))} for c in card.words]
        self.trns = [{k: v for (k, v) in zip(('id','text', 'type'),
                                             (c.id, c.text, type(c)))} for c in card.translations]

        self.sf = session_factory

        self.s = ttk.Style(master)
        self.set_styles()

        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Variables for card desplays
        self.card_title = tk.StringVar()
        self.card_example = tk.StringVar()
        self.card_translation = tk.StringVar()

        # current index for example and translation displays
        self.ex_ind = 0
        self.trn_ind = 0

        self.card_title.set(self.card_text)
        self.create_widgets()

    def set_styles(self):
        self.s.map('TButton',
                    foreground=[('disabled','#a3a3a3')],
                   relief=[('!disabled','pressed','sunken')])

    def create_widgets(self):

        #Title Content
        self.title_frame = ttk.Frame(self, borderwidth=2, relief='solid', padding=2)
        self.title_frame.grid(row=0, column=0, sticky=tk.N)
        self.title = tk.Text(self.title_frame, width=40, height=5, state="disabled", wrap="word")
        self.update_text(self.title, self.card_title.get())
        self.title.grid(column=0, row=0, sticky=tk.N)

        self.title_scroll = ttk.Scrollbar(self.title_frame,
                                          orient=tk.VERTICAL,
                                          command=self.title.yview)
        self.title.configure(yscrollcommand=self.title_scroll.set)

        self.title_scroll.grid(column=1,row=0,sticky=(tk.N, tk.S))

        self.title_edit_frame = ttk.Frame(self.title_frame, borderwidth=2, relief='solid', padding=2)
        self.title_edit_frame.grid(row=1, column=0)

        self.title_edit_button = ttk.Button(self.title_edit_frame,
                                            text="Edit Title",
                                            command=self.title_edit_call)
        self.title_edit_button.grid(column=0, row=0, sticky=tk.N)

        self.title_save_button = ttk.Button(self.title_edit_frame,
                                            text="Save Change",
                                            command=self.title_save_call,
                                            state='disabled')
        self.title_save_button.grid(column=1, row=0, sticky=tk.N)
        self.title_nosave_button = ttk.Button(self.title_edit_frame,
                                              text="Discard Change",
                                              command=self.title_nosave_call,
                                              state='disabled')
        self.title_nosave_button.grid(column=2, row=0, sticky=tk.N)

        self.content_frame = ttk.Frame(self, borderwidth=2, relief='solid', padding="0 10 0 0")
        self.content_frame.grid(row=1, column=0, sticky=tk.N)
        #self.content_frame.columnconfigure(1)

        #example frames
        self.example_frame = ttk.Frame(self.content_frame, borderwidth=2, relief="solid", padding="2 10")
        self.example_frame.grid(row=0, column=0, sticky=tk.NW)

        self.ex_entry_frame = ttk.Frame(self.example_frame, borderwidth=2, relief='solid', padding=2)
        self.ex_entry_frame.grid(row=0, column=0, sticky=tk.N)

        self.ex_button_frame = ttk.Frame(self.example_frame, borderwidth=2, relief='solid', padding=2)
        self.ex_button_frame.grid(row=0, column=1, sticky=tk.N)

        self.ex_np_button_frame = ttk.Frame(self.ex_button_frame, borderwidth=2, relief='solid', padding=0)
        self.ex_np_button_frame.grid(row=0, column=0, sticky=tk.N)

        self.ex_hs_button_frame = ttk.Frame(self.ex_button_frame, borderwidth=2, relief='solid', padding=2)
        self.ex_hs_button_frame.grid(row=0, column=1, sticky=tk.N)
        self.ex_hs_button_frame.columnconfigure(0, minsize="3.5c")

        self.ex_card_select_frame = ttk.Frame(self.ex_button_frame, borderwidth=2, relief='solid', padding=2)
        self.ex_card_select_frame.grid(row=0, column=2, sticky=tk.N)
        self.ex_card_select_frame.columnconfigure(0, minsize="3c")

        self.ex_edit_frame = ttk.Frame(self.ex_button_frame, borderwidth=2, relief='solid', padding=2)
        self.ex_edit_frame.grid(row=1, column=0, columnspan=3, sticky=tk.N)


        # Translation Frames
        self.translation_frame = ttk.Frame(self.content_frame, borderwidth=2, relief="solid", padding="2 10")
        self.translation_frame.grid(row=1, column=0, sticky=tk.N)

        self.tr_entry_frame = ttk.Frame(self.translation_frame, borderwidth=2, relief='solid', padding=2)
        self.tr_entry_frame.grid(row=0, column=0, sticky=tk.N)

        self.tr_button_frame = ttk.Frame(self.translation_frame, borderwidth=2, relief='solid', padding=2)
        self.tr_button_frame.grid(row=0, column=1, sticky=tk.N)

        self.tr_np_button_frame = ttk.Frame(self.tr_button_frame, borderwidth=2, relief='solid', padding=0)
        self.tr_np_button_frame.grid(row=0, column=1, sticky=tk.N)

        self.tr_hs_button_frame = ttk.Frame(self.tr_button_frame, borderwidth=2, relief='solid', padding=2)
        self.tr_hs_button_frame.grid(row=0, column=2, sticky=tk.N)
        self.tr_hs_button_frame.columnconfigure(0, minsize="3.5c")

        self.tr_card_select_frame = ttk.Frame(self.tr_button_frame, borderwidth=2, relief='solid', padding=2)
        self.tr_card_select_frame.grid(row=0, column=3, sticky=tk.N)
        self.tr_card_select_frame.columnconfigure(0, minsize="3c")

        self.tr_edit_frame = ttk.Frame(self.tr_button_frame, borderwidth=2, relief='solid', padding=2)
        self.tr_edit_frame.grid(row=1, column=0, columnspan=3, sticky=tk.N)

        # Example buttons and fields
        self.example_label = ttk.Label(self.ex_entry_frame,text="example: ", padding=2)
        self.example = tk.Text(self.ex_entry_frame, width=40, height=5, wrap="word", state="disabled")
        self.example_scrollbar = ttk.Scrollbar(self.ex_entry_frame,
                                          orient=tk.VERTICAL,
                                          command=self.example.yview)
        self.example.configure(yscrollcommand=self.example_scrollbar.set)
        self.show_example = ttk.Button(self.ex_hs_button_frame,
                                       text="Show {example}".format(example=maps.card_example_fields.
                                                                    get(type(self.card),"")),
                                       command=self.show_example_but)
        self.hide_example = ttk.Button(self.ex_hs_button_frame,
                                       text="Show {example}".format(example=maps.card_example_fields.
                                                                    get(type(self.card), "")),
                                       command=self.hide_ex)
        self.next_example = ttk.Button(self.ex_np_button_frame, text="Next", command=self.next_ex, state='disabled')
        self.prev_example = ttk.Button(self.ex_np_button_frame, text="Prev", command=self.prev_ex, state='disabled')
        self.select_example = ttk.Button(self.ex_card_select_frame,
                                         text="Select Example",
                                         state='disabled',
                                         command=self.select_example_but)
        self.add_example = ttk.Button(self.ex_edit_frame, text="Add Example", command=self.add_example_call)
        self.remove_example = ttk.Button(self.ex_edit_frame, text="Remove Example", command=self.remove_example_call)


        # Translation Buttons and fields
        self.show_translation = ttk.Button(self.tr_hs_button_frame, text="Show Translations",
                                           command=self.show_translation_but)
        self.translation_label = ttk.Label(self.tr_entry_frame, text="translation: ", borderwidth=2)
        self.translations = tk.Text(self.tr_entry_frame, width=40, height=5, wrap="word", state="disabled")
        self.translation_scrollbar = ttk.Scrollbar(self.tr_entry_frame,
                                          orient=tk.VERTICAL,
                                          command=self.translations.yview)
        self.translations.configure(yscrollcommand=self.translation_scrollbar.set)
        self.next_translation = ttk.Button(self.tr_np_button_frame, text="Next", command=self.next_tr, state='disabled')
        self.prev_translation = ttk.Button(self.tr_np_button_frame, text="Prev", command=self.prev_tr, state='disabled')
        self.hide_translation = ttk.Button(self.tr_hs_button_frame, text="Hide Translations",
                                           command=self.hide_translation_but)
        self.select_translation = ttk.Button(self.tr_card_select_frame,
                                             text="Select Translation",
                                             state="disabled",
                                             command=self.select_translation_but)
        self.add_translation = ttk.Button(self.tr_edit_frame, text="Add Translation",
                                          command=self.add_translation_call)
        self.remove_translation = ttk.Button(self.tr_edit_frame, text="Remove Translation",
                                             command=self.remove_translation_call)

        #gridding of items
        self.example_label.grid(column=0, row=0, sticky=tk.N)
        self.show_example.grid(column=0, row=0, sticky=tk.NW)
        self.next_example.grid(column=1, row=0, sticky=(tk.N, tk.NW))
        self.prev_example.grid(column=0, row=0, sticky=(tk.N, tk.NW))
        self.hide_example.grid(column=0, row=0, sticky=(tk.N, tk.NW))
        self.example.grid(column=1, row=0)
        self.example_scrollbar.grid(column=2, row=0, sticky=(tk.N, tk.S))
        self.add_example.grid(column=0, row=0, sticky=tk.N)
        self.remove_example.grid(column=1, row=0, sticky=tk.N)
        self.ex_entry_frame.columnconfigure(0, minsize="3c")
        self.tr_entry_frame.columnconfigure(0, minsize="3c")
        self.hide_example.grid_remove()

        self.show_translation.grid(column=0, row=0, sticky=tk.NW)
        self.translation_label.grid(column=0, row=0, stick=tk.N)
        self.translations.grid(column=1, row=0)
        self.translation_scrollbar.grid(column=2, row=0, sticky=(tk.N, tk.S))
        self.add_translation.grid(column=0, row=0, sticky=tk.N)
        self.remove_translation.grid(column=1, row=0, sticky=tk.N)

        self.prev_translation.grid(column=0, row=0, sticky=(tk.N, tk.NW))
        self.next_translation.grid(column=1, row=0, sticky=(tk.N, tk.NW))
        self.hide_translation.grid(column=0, row=0, sticky=(tk.N, tk.NW))
        self.hide_translation.grid_remove()

        self.select_example.grid(column=0, row=0, sticky=tk.NW)
        self.select_translation.grid(column=0, row=0, sticky=tk.NW)

        self.clear_text(self.example)
        self.clear_text(self.translations)
            

    def next_tr(self):
        if self.trns:
            self.trn_ind = (self.trn_ind + 1)%len(self.trns)
            self.update_text(self.translations, self.trns[min(len(self.trns) - 1, self.trn_ind)].get('text'))

    def prev_tr(self):
        if self.trns:
            self.trn_ind = (self.trn_ind - 1) % len(self.trns)
            self.update_text(self.translations, self.trns[min(len(self.trns) - 1, self.trn_ind)].get('text'))

    def show_example_but(self):
        self.show_example.grid_remove()
        self.next_example['state'] = 'normal'
        self.prev_example['state'] = 'normal'
        self.select_example['state'] = 'normal'
        if self.examples:
            self.update_text(self.example, self.examples[self.ex_ind].get('text'))
        self.hide_example.grid()
        self.example.grid()

    def show_translation_but(self):
        self.show_translation.grid_remove()
        self.translations.grid()
        self.prev_translation['state'] = 'normal'
        self.next_translation['state'] = 'normal'
        self.select_translation['state'] = 'normal'
        if self.trns:
            self.update_text(self.translations, self.trns[min(len(self.trns)-1, self.trn_ind)].get('text'))
        self.hide_translation.grid()

    def hide_translation_but(self):
        self.show_translation.grid()
        self.prev_translation['state'] = 'disabled'
        self.next_translation['state'] = 'disabled'
        self.select_translation['state'] = 'disabled'
        self.clear_text(self.translations)
        self.hide_translation.grid_remove()

    def next_ex(self):
        if self.examples:
            self.ex_ind = (self.ex_ind + 1)%len(self.examples)
            self.update_text(self.example, self.examples[self.ex_ind].get('text'))

    def prev_ex(self):
        if self.examples:
            self.ex_ind = (self.ex_ind - 1) % len(self.examples)
            self.update_text(self.example, self.examples[self.ex_ind].get('text'))

    def hide_ex(self):
        self.show_example.grid()
        self.prev_example['state'] = 'disabled'
        self.next_example['state'] = 'disabled'
        self.select_example['state'] = 'disabled'
        self.clear_text(self.example)
        self.hide_example.grid_remove()

    def select_example_but(self):
        with session_scope(self.sf) as sess:
            self.root.new_card_view(sess, self.examples[self.ex_ind], self.sf)

    def select_translation_but(self):
        with session_scope(self.sf) as sess:
            self.root.new_card_view(sess, self.trns[self.trn_ind], self.sf)

    def title_edit_call(self):
        self.title_save_button['state'] = 'normal'
        self.title_nosave_button['state'] = 'normal'
        self.title_edit_button['state'] = 'disabled'
        self.title["state"] = "normal"


    def title_save_call(self):
        self.title_save_button['state'] = 'disabled'
        self.title_nosave_button['state'] = 'disabled'
        self.title_edit_button['state'] = 'normal'
        self.card_title.set(self.title.get("1.0", "end"))
        self.card_text = self.card_title.get()
        self.title["state"] = "disabled"

        # update database
        if self.sf:
            with session_scope(self.sf) as sess:
                self.edit_title(sess,  self.card_title.get())

        self.update_signal()

    def title_nosave_call(self):
        self.title_save_button['state'] = 'disabled'
        self.title_nosave_button['state'] = 'disabled'
        self.title_edit_button['state'] = 'normal'
        self.update_text(self.title, self.card_title.get())
        self.title["state"] = "disabled"

    def add_example_call(self):
        """Triggers the add example window"""
        tl = tk.Toplevel()

        with session_scope(self.sf) as sess:
            cd = sess.query(self.card_type).filter_by(id=self.card_id).one()
            MapDeckView(cd, "example", tl, self, self.sf)

    def remove_example_call(self):
        """Triggers the remove example call"""

    def add_translation_call(self):
        """Triggers the Add Translation call"""
        tl = tk.Toplevel()

        with session_scope(self.sf) as sess:
            cd = sess.query(self.card_type).filter_by(id=self.card_id).one()
            MapDeckView(cd, "translation", tl, self, self.sf)

    def remove_translation_call(self):
        """Triggers the Remove Translation call"""

    def new_card_view(self, sess, card,  sf):
        t = tk.Toplevel(self.master)
        cd = sess.query(card.get('type')).filter_by(id=card.get('id')).one()
        new_window = CardView(cd, t, sf, root=self.root)
        self.descendants = self.descendants + (new_window,)

    def edit_title(self, sess, text):
        cd = sess.query(self.card_type).filter_by(id=self.card_id).one()
        cd.text = text

    def update_signal(self):
        if self.root:
            self.root.view_update()

    def view_update(self):
        self.update_self()


    def update_self(self):
        with session_scope(self.sf) as sess:
            self._update_self(sess)

        for c in self.descendants:
            c.view_update()

    def _update_self(self, sess):
        card = sess.query(self.card_type).filter_by(id=self.card_id).one()
        if type(card) == Cards.LanguageAVocab or type(card) == Cards.LanguageBVocab:
            self.examples = [{k: v for (k, v) in zip(('id','text', 'type'),
                                                     (c.id, c.text, type(c)))} for c in card.examples]
        else:
            self.examples = [{k: v for (k, v) in zip(('id','text', 'type'),
                                                     (c.id, c.text, type(c)))} for c in card.words]
        self.trns = [{k: v for (k, v) in zip(('id','text', 'type'),
                                             (c.id, c.text, type(c)))} for c in card.translations]

        if self.trns:
            self.update_text(self.translations, self.trns[min(len(self.trns) - 1, self.trn_ind)].get('text'))
        if self.examples:
            self.update_text(self.example, self.examples[min(self.ex_ind,len(self.examples))].get('text'))

        self.update_text(self.title,card.text)
        self.card_title.set(card.text)
        self.card_text = card.text

    def update_text(self, text_widget, string):
        """update the text in the given text widget to string, returning the state of the widget
        to its prior state when finished"""
        state = text_widget["state"]
        text_widget["state"] = "normal"
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", string)
        text_widget["state"] = state

    def clear_text(self,text_widget):
        self.update_text(text_widget,"")

    def map_update(self):
        self.update_self()


class Browse_Card_View(CardView):
    """Card view without options of editing, card selection or hiding cards"""
    def __init__(self, card, master=None, session_factory=None, root=None, descendants=()):
        super().__init__(card, master, session_factory, root, descendants)
        self.show_example_but()
        self.show_translation_but()
        self.hide_translation.grid_remove()
        self.hide_example.grid_remove()
        self.select_example.grid_remove()
        self.select_translation.grid_remove()
        self.title_edit_button.grid_remove()
        self.title_save_button.grid_remove()
        self.title_nosave_button.grid_remove()
        self.ex_edit_frame.grid_remove()
        self.tr_edit_frame.grid_remove()


class Add_Card_View(CardView):
    """View for adding card"""
    def __init__(self, card, deck_id, master=None, session_factory=None, root=None, descendants=()):
        super().__init__(card, master, session_factory, root, descendants)
        self.content_frame.grid_remove()

        self.card_type = ttk.Combobox(self.title_edit_frame)
        self.card_type['values'] = [maps.type_names[key] for key in maps.type_names]
        self.card_type['state'] = "readonly"
        self.card_type.grid(row=1, column=0, sticky=tk.E)

        self.deck_id = deck_id


    def title_save_call(self):
        self.title_save_button['state'] = 'disabled'
        self.title_nosave_button['state'] = 'disabled'
        self.title_edit_button['state'] = 'normal'
        self.card_title.set(self.title.get("1.0", "end"))
        self.card_text = self.card_title.get()
        self.title["state"] = "disabled"

        #update database
        if self.sf:
            with session_scope(self.sf) as sess:
                self.edit_title(sess,  self.card_title.get())

        self.update_signal()
        self.master.destroy()

    def edit_title(self, sess, title):
        cd = maps.type_names_to_cards[self.card_type.get()](text=title)
        deck = sess.query(decks.Deck).filter_by(id=self.deck_id).one()
        sess.add(cd)
        sess.commit()
        deck_ui.add_card(deck,cd)

    def update_signal(self):
        if self.root:
            self.root.update()






class MapDeckView(ttk.Frame):
    """View for Editing Mappings for a given Card"""

    def __init__(self, card, map_type=None, master=None, report_dest=None, session_factory=None):
        super().__init__(master, padding=5)
        self.session_factory = session_factory
        self.report_dest = report_dest
        self.card = card

        assert issubclass(type(report_dest), CardView), "master must be cdview.CardView"

        self.card_id = card.id
        assert map_type in ["example", "translation"], "must specify type"

        if map_type == "example":
            self.card_type = maps.card_example_types.get(type(card))
            self.map_attribute = maps.card_example_fields[type(card)]
            maplist = getattr(card, maps.card_example_fields[type(card)],[])
        else:
            self.card_type = maps.card_translation_types.get(type(card))
            self.map_attribute = "translations"
            maplist = getattr(card, "translations",[])

        self.mapped = sorted([{t: k for (t, k) in
                             zip(("id", "text", "type", "tree_id"),
                             (c.id, c.text, type(c), self.tree_id(c.text, c.id)))}
                                  for c in maplist],
                             key=lambda x: str.lower(x.get("text", "")))
        self.report = {i.get("id"): None for i in self.mapped}

        with session_scope(self.session_factory) as sess:
            self.card_pool = self.get_card_pool(sess, self.card_type)

        # Grid Self
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Define Text Variables
        self.title_var = tk.StringVar()
        self.pool_title_var = tk.StringVar()
        self.map_title_var  = tk.StringVar()

        # Define Frames
        self.title_frame    = ttk.Frame(self,  borderwidth=2, relief="solid", padding="2 2 2 5")
        self.content_frame  = ttk.Frame(self,  borderwidth=2, relief="solid", padding="2 5 2 2")
        self.view_frame     = ttk.Frame(self, borderwidth=2, relief="solid", padding="2 2 2 2")
        self.pool_frame     = ttk.Frame(self.content_frame, borderwidth=2, relief="solid", padding="2 2 2 2")
        self.button_frame   = ttk.Frame(self.content_frame, borderwidth=2, relief="solid", padding="2 2 2 2")
        self.mapped_frame   = ttk.Frame(self.content_frame, borderwidth=2, relief="solid", padding="2 2 2 2")


        # Define Widgets
        self.title = ttk.Label(self.title_frame, textvariable=self.title_var)
        self.pool_title = ttk.Label(self.pool_frame, textvariable=self.pool_title_var)
        self.pool = ttk.Treeview(self.pool_frame, selectmode="browse")
        self.pool_scroll = ttk.Scrollbar(self.pool_frame,
                                         orient=tk.VERTICAL,
                                         command=self.pool.yview)
        self.pool.configure(yscrollcommand=self.pool_scroll.set)
        self.add_button = ttk.Button(self.button_frame,
                                     text="Add Card >>>",
                                     command=self.add_button_call)
        self.remove_button = ttk.Button(self.button_frame,
                                        text="<<< Remove Card",
                                        command=self.remove_button_call)
        self.done_button = ttk.Button(self.button_frame,
                                      text="Done",
                                      command=self.done_call)
        self.map_title = ttk.Button(self.mapped_frame, textvariable=self.map_title_var)
        self.map = ttk.Treeview(self.mapped_frame)
        self.map_scroll = ttk.Scrollbar(self.mapped_frame,
                                        orient=tk.VERTICAL,
                                        command=self.map.yview)
        self.map.configure(yscrollcommand=self.map_scroll.set)

        # Grid Widgets
        self.title_frame.grid(column=0, row=0, sticky=tk.N)
        self.content_frame.grid(column=0, row=1, sticky=tk.N)
        self.view_frame.grid(column=0, row=2, sticky=tk.S)
        self.pool_frame.grid(column=0, row=0, sticky=(tk.N, tk.S))
        self.button_frame.grid(column=1, row=0, sticky=(tk.W, tk.E))
        self.mapped_frame.grid(column=2, row=0, sticky=(tk.N, tk.S))


        self.title.grid(column=0, row=0, sticky=tk.N)

        self.pool_title.grid(column=0, row=0, sticky=tk.N)
        self.pool.grid(column=0, row=1, sticky=tk.N)
        self.pool_scroll.grid(column=1, row=1, sticky=(tk.N, tk.S))

        self.add_button.grid(column=0, row=0, sticky=(tk.W, tk.E))
        self.remove_button.grid(column=0, row=1, sticky=(tk.W, tk.E))
        self.done_button.grid(column=0, row=2, sticky=(tk.W, tk.E))

        self.map_title.grid(column=0, row=0, sticky=tk.N)
        self.map.grid(column=0, row=1, sticky=tk.N)
        self.map_scroll.grid(column=1, row=1, sticky=(tk.N, tk.S))

        # Add view triggers
        self.pool.tag_bind("card","<<TreeviewSelect>>", self.select_call)

        self.title_var.set(maps.card_example_fields[type(card)] +" for " + card.text)
        self.pool_title_var.set("pool of " + maps.card_example_fields[type(card)])
        self.map_title_var.set("mapped " + maps.card_example_fields[type(card)])

        self.pool.insert("", "end", "pool", text="", open=True)
        self.map.insert("", "end", "map", text="", open=True)

        #populate lists
        self.update_lists()

    def update_lists(self):
        self.pool.delete("pool")
        self.map.delete("map")
        self.pool.insert("", "end", "pool", text="", open=True)
        self.map.insert("", "end", "map", text="", open=True)
        for item in self.card_pool:
            self.pool.insert("pool", "end",item.get("tree_id"), text=item.get("text"), tags=("card",))
        for item in self.mapped:
            self.map.insert("map", "end", item.get("tree_id"), text=item.get("text"), tags=("card",))

    def add_button_call(self):
        item = self.pool.selection()[0]
        pitem = self.parsed_card(item)
        if not pitem[1] in self.report:
            self.report[pitem[1]] = None
            self.map.insert("map", "end", item, text=pitem[0])


    def remove_button_call(self):
        item = self.map.selection()[0]
        pitem = self.parsed_card(item)
        self.map.delete(item)
        self.report.pop(pitem[1], None)

    def tree_id(self, text, item_id):
        return text + "|," + str(item_id)

    def parsed_card(self, item):
        split_item = item.split("|,")
        split_item[1] = int(split_item[1])
        return split_item

    def get_card_pool(self, sess, card_type):
        cards = sess.query(card_type).all()
        return sorted([{t: k for (t, k) in
                      zip(("id", "text", "type", "tree_id"),
                      (c.id, c.text, type(c), self.tree_id(c.text, c.id)))}
                          for c in cards],
                      key=lambda x: str.lower(x.get("text", "")))

    def select_call(self, event):
        """Opens a Browse view of selected card from treeview"""
        card_info = event.widget.selection()[0]
        print(card_info)

        with session_scope(self.session_factory) as sess:
            card = self.get_card(card_info, sess)
            Browse_Card_View(card, self.view_frame, self.session_factory)

        print("Card Browsing")

    def get_card(self, card_info, sess):
        card_id = self.parsed_card(card_info)[1]
        return sess.query(self.card_type).filter_by(id=card_id).one()

    def done_call(self):
        """Destroy current view.  commit changes to cards mappings"""
        updates = {"type": self.card_type, "ids": self.report, "card": self.card}
        with session_scope(self.session_factory) as sess:
            c = sess.query(type(self.card)).filter_by(id=self.card_id).one()
            if self.report.keys():
                update = sess.query(self.card_type).filter(self.card_type.id.in_(self.report)).all()
            else:
                update = []
            setattr(c, self.map_attribute, update)

        self.report_dest.map_update()
        self.master.destroy()








