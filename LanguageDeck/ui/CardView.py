import tkinter as tk
import tkinter.ttk as ttk
from LanguageDeck.models import Cards
from LanguageDeck.session_tools.session_scope import session_scope


class CardView(ttk.Frame):
    def __init__(self, card, master=None, session_factory=None, root=None, descendants=()):
        super().__init__(master, padding=5)
        # tree relationships
        self.root = root if root else self
        self.descendants = descendants

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
        self.title = tk.Text(self.title_frame, width=40, height=5, state="disabled")
        self.update_text(self.title, self.card_title.get())
        self.title.grid(column=0, row=0, sticky=tk.N)

        self.title_scroll = ttk.Scrollbar(self.title_frame,
                                          orient=tk.VERTICAL,
                                          command=self.title.yview,
                                          wrap="word")
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

        self.ex_np_button_frame = ttk.Frame(self.example_frame, borderwidth=2, relief='solid', padding=0)
        self.ex_np_button_frame.grid(row=0, column=1, sticky=tk.N)

        self.ex_hs_button_frame = ttk.Frame(self.example_frame, borderwidth=2, relief='solid', padding=2)
        self.ex_hs_button_frame.grid(row=0, column=2, sticky=tk.N)
        self.ex_hs_button_frame.columnconfigure(0, minsize="3.5c")

        self.ex_card_select_frame = ttk.Frame(self.example_frame, borderwidth=2, relief='solid', padding=2)
        self.ex_card_select_frame.grid(row=0, column=3, sticky=tk.N)
        self.ex_card_select_frame.columnconfigure(0, minsize="3c")

        # Translation Frames
        self.translation_frame = ttk.Frame(self.content_frame, borderwidth=2, relief="solid", padding="2 10")
        self.translation_frame.grid(row=1, column=0, sticky=tk.N)

        self.tr_entry_frame = ttk.Frame(self.translation_frame, borderwidth=2, relief='solid', padding=2)
        self.tr_entry_frame.grid(row=0, column=0, sticky=tk.N)

        self.tr_np_button_frame = ttk.Frame(self.translation_frame, borderwidth=2, relief='solid', padding=0)
        self.tr_np_button_frame.grid(row=0, column=1, sticky=tk.N)

        self.tr_hs_button_frame = ttk.Frame(self.translation_frame, borderwidth=2, relief='solid', padding=2)
        self.tr_hs_button_frame.grid(row=0, column=2, sticky=tk.N)
        self.tr_hs_button_frame.columnconfigure(0, minsize="3.5c")

        self.tr_card_select_frame = ttk.Frame(self.translation_frame, borderwidth=2, relief='solid', padding=2)
        self.tr_card_select_frame.grid(row=0, column=3, sticky=tk.N)
        self.tr_card_select_frame.columnconfigure(0, minsize="3c")

        # Example buttons and fields
        self.example_label = ttk.Label(self.ex_entry_frame,text="example: ", padding=2)
        self.example = tk.Text(self.ex_entry_frame, width=40, height=5, wrap="word", state="disabled")
        self.example_scrollbar = ttk.Scrollbar(self.ex_entry_frame,
                                          orient=tk.VERTICAL,
                                          command=self.example.yview)
        self.example.configure(yscrollcommand=self.example_scrollbar.set)
        self.show_example = ttk.Button(self.ex_hs_button_frame, text="Show Examples", command=self.show_example_but)
        self.hide_example = ttk.Button(self.ex_hs_button_frame, text="Hide Example", command=self.hide_ex)
        self.next_example = ttk.Button(self.ex_np_button_frame, text="Next", command=self.next_ex, state='disabled')
        self.prev_example = ttk.Button(self.ex_np_button_frame, text="Prev", command=self.prev_ex, state='disabled')
        self.select_example = ttk.Button(self.ex_card_select_frame,
                                         text="Select Example",
                                         state='disabled',
                                         command=self.select_example_but)


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

        #gridding of items
        self.example_label.grid(column=0, row=0, sticky=tk.N)
        self.show_example.grid(column=0, row=0, sticky=tk.NW)
        self.next_example.grid(column=1, row=0, sticky=(tk.N, tk.NW))
        self.prev_example.grid(column=0, row=0, sticky=(tk.N, tk.NW))
        self.hide_example.grid(column=0, row=0, sticky=(tk.N, tk.NW))
        self.example.grid(column=1, row=0)
        self.example_scrollbar.grid(column=2, row=0, sticky=(tk.N, tk.S))
        self.ex_entry_frame.columnconfigure(0, minsize="3c")
        self.tr_entry_frame.columnconfigure(0, minsize="3c")
        self.hide_example.grid_remove()

        self.show_translation.grid(column=0, row=0, sticky=tk.NW)
        self.translation_label.grid(column=0, row=0, stick=tk.N)
        self.translations.grid(column=1, row=0)
        self.translation_scrollbar.grid(column=2, row=0, sticky=(tk.N, tk.S))

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

        #update database
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











