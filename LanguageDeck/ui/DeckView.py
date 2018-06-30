"""
DeckView is the primary gui for the Deck object.  Essentially it is just a listbox.
"""

import tkinter as tk
import tkinter.ttk as ttk
import LanguageDeck.ui.CardView as card_view
import LanguageDeck.models as models
import LanguageDeck.session_tools.session_scope as sessc


# TODO make type names configurable
type_names = {"vocab a": "vocab a",
              "vocab b": "vocab b",
              "example a": "example a",
              "example b": "example b"}

type_abbreviations = {"ea": models.Cards.LanguageAExample,
                      "eb": models.Cards.LanguageBExample,
                      "va": models.Cards.LanguageAVocab,
                      "vb": models.Cards.LanguageBVocab}

#TODO Implement Root logic for Decks
class DeckView(ttk.Frame):
    def __init__(self, deck, master=None, session_factory=None, **kwargs):
        super().__init__(master, padding=5)
        self.vertical_offset = 0
        self.session_factory = session_factory
        # Placement of master frame
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.deck_id = deck.id

        # Deck contents
        self.vocab_a = sorted([{t: k for (t, k) in
                              zip(("id", "text", "type", "tree_id"),
                                  (c.id, c.text, type(c), self.tree_id(type(c), c.id)))}
                              for c in deck.vocab_a],
                              key=lambda x: str.lower(x.get("text", "")))
        self.vocab_b = sorted([{t: k for (t, k) in
                              zip(("id", "text", "type", "tree_id"),
                                  (c.id, c.text, type(c), self.tree_id(type(c), c.id)))}
                              for c in deck.vocab_b],
                              key=lambda x: str.lower(x.get("text", "")))

        self.examples_a = sorted([{t: k for (t, k) in
                                 zip(("id", "text", "type", "tree_id"),
                                     (c.id, c.text, type(c), self.tree_id(type(c), c.id)))}
                                 for c in deck.examples_a],
                                 key=lambda x: str.lower(x.get("text", "")))
        self.examples_b = sorted([{t: k for (t, k) in
                                 zip(("id", "text", "type", "tree_id"),
                                     (c.id, c.text, type(c), self.tree_id(type(c), c.id)))}
                                 for c in deck.examples_b],
                                 key=lambda x: str.lower(x.get("text", "")))
        self.card_dict = {k: v for (k, v) in [(c.get("tree_id"), c) for c in
                                              self.vocab_a + self.vocab_b + self.examples_a + self.examples_b]}
        self.name = deck.name

        self.title_variable = tk.StringVar()
        self.title_variable.set(self.name)

        # Frames
        self.title_frame = ttk.Frame(self, borderwidth=2, relief="solid", padding="2 2 2 10")
        self.content_frame = ttk.Frame(self, borderwidth=2, relief="solid", padding="2 2 2 10")
        self.tree_frame = ttk.Frame(self.content_frame, borderwidth=2, relief="solid", padding="2 2 2 5")
        self.tree_button_frame = ttk.Frame(self.content_frame, borderwidth=2, relief="solid", padding="2 0 2 10")

        # Content widgets
        self.title = ttk.Label(self, textvariable=self.title_variable)
        self.tree_list = ttk.Treeview(self.tree_frame)
        self.tree_scroll = ttk.Scrollbar(self.tree_frame,
                                         orient=tk.VERTICAL,
                                         command=self.tree_list.yview)
        self.tree_list.configure(yscrollcommand=self.tree_scroll.set,
                                 selectmode="browse")
        self.add_button = ttk.Button(self.tree_button_frame,
                                     text="Add Card",
                                     command=self.add_button_call)
        self.create_button = ttk.Button(self.tree_button_frame,
                                        text="Create Card",
                                        command=self.create_button_call)
        self.remove_button = ttk.Button(self.tree_button_frame,
                                        text="Remove Button",
                                        command=self.remove_button_call)
        self.select_button = ttk.Button(self.tree_button_frame,
                                        text="Select Button",
                                        command=self.select_button_call)

        # Grid
        self.title_frame.grid(row=0, column=0, sticky=tk.N)
        self.title.grid(row=0, column=0, sticky=tk.N)
        self.content_frame.grid(row=1, column=0, sticky=tk.NW)
        self.tree_frame.grid(row=0, column=0, sticky=tk.N)
        self.tree_button_frame.grid(row=1, column=0, sticky=tk.N)

        self.title.grid(row=0, column=0, sticky=tk.N)
        self.tree_list.grid(row=0, column=0, sticky=tk.NW)
        self.tree_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.add_button.grid(row=0, column=0, sticky=tk.N)
        self.create_button.grid(row=0, column=1, sticky=tk.N)
        self.remove_button.grid(row=0, column=2, sticky=tk.N)
        self.select_button.grid(row=0, column=3, sticky=tk.N)

        # Populate tree
        self.populate_tree()

    def populate_tree(self):
        """populates the empty tree"""
        self.populate_category(type_names["vocab a"], self.vocab_a)
        self.populate_category(type_names["vocab b"], self.vocab_b)
        self.populate_category(type_names["example a"], self.examples_a)
        self.populate_category(type_names["example b"], self.examples_b)

    def populate_category(self, name, items):
        """populates tree with items in list"""
        self.tree_list.insert("", "end", name, text=name)
        for i in items:
            self.tree_list.insert(name, "end",
                                  i.get("tree_id"),
                                  text=i.get("text")[:30],
                                  tags=("card",))

    def update_list(self):
        pass

    def add_button_call(self):
        pass


    def create_button_call(self):
        tl = tk.Toplevel()
        acv = card_view.Add_Card_View(models.Cards.LanguageAVocab(text=""), self.deck_id,
                            master=tl,
                            session_factory=self.session_factory,
                            root=self,
                            descendants=())

    def remove_button_call(self):
        pass

    def select_button_call(self):
        pass

    def update(self):
        with sessc.session_scope(self.session_factory) as sess:
            self._update(sess)

    def _update(self, sess):
        deck = sess.query(models.decks.Deck).filter_by(id=self.deck_id).one()

        # Deck contents
        self.vocab_a = sorted([{t: k for (t, k) in
                                zip(("id", "text", "type", "tree_id"),
                                    (c.id, c.text, type(c), self.tree_id(type(c), c.id)))}
                               for c in deck.vocab_a],
                              key=lambda x: str.lower(x.get("text", "")))
        self.vocab_b = sorted([{t: k for (t, k) in
                                zip(("id", "text", "type", "tree_id"),
                                    (c.id, c.text, type(c), self.tree_id(type(c), c.id)))}
                               for c in deck.vocab_b],
                              key=lambda x: str.lower(x.get("text", "")))

        self.examples_a = sorted([{t: k for (t, k) in
                                   zip(("id", "text", "type", "tree_id"),
                                       (c.id, c.text, type(c), self.tree_id(type(c), c.id)))}
                                  for c in deck.examples_a],
                                 key=lambda x: str.lower(x.get("text", "")))
        self.examples_b = sorted([{t: k for (t, k) in
                                   zip(("id", "text", "type", "tree_id"),
                                       (c.id, c.text, type(c), self.tree_id(type(c), c.id)))}
                                  for c in deck.examples_b],
                                 key=lambda x: str.lower(x.get("text", "")))

        for item in type_names:
            self.tree_list.delete(type_names[item])

        self.populate_tree()

    @staticmethod
    def tree_id(t, i):
        if t == models.Cards.LanguageAVocab:
            return "va," + str(i)
        elif t == models.Cards.LanguageBVocab:
            return "vb," + str(i)
        elif t == models.Cards.LanguageAExample:
            return "ea," + str(i)
        elif t == models.Cards.LanguageBExample:
            return "eb," + str(i)
        else:
            return Exception()

    def map_update(self, update_dict):
        pass

class BrowseDeckView(DeckView):
    """
    Subdeck class which displays deck view in browse mode
    """
    def __init__(self, deck, master=None, session_factory=None, select_call=None, **kwargs):
        super().__init__(deck, master, session_factory, **kwargs)
        self.browse_window = None
        self.tree_list.tag_bind("card", "<<TreeviewSelect>>", self.browse_select_call)

        # Browse window
        self.browse_frame = ttk.Frame(self,
                                      borderwidth=2,
                                      relief="solid",
                                      padding="5 2 2 10")

        self.browse_frame.grid(row=1, column=1, sticky=tk.NE)

        self.select_call = select_call if select_call else self.default_select_call
        self.select_button.configure(command=self.select_call)

        self.open_windows = {}
        self.open_cards = {}

    def browse_select_call(self, event):
        """view selected card in browse mode"""
        card_info = event.widget.selection()

        with sessc.session_scope(self.session_factory) as sess:
            card = self.get_card(card_info, sess)
            card_view.Browse_Card_View(card, self.browse_frame, self.session_factory)

        print("Card Browsing")

    @staticmethod
    def get_card(crd, sess):
        parsed_crd = crd[0].split(",")
        card_type = type_abbreviations.get(parsed_crd[0])
        card_id = parsed_crd[1]

        return sess.query(card_type).filter_by(id=card_id).one()

    def default_select_call(self):
        window = tk.Toplevel()
        self.open_windows[window] = None
        window.bind("<Destroy>", self.destroyed_window)
        with sessc.session_scope(self.session_factory) as sess:
            c_id = self.tree_list.selection()
            card = self.get_card(c_id, sess)
            if c_id in self.open_cards:
                window.destroy()
                self.open_cards[c_id].lift()
                self.open_cards[c_id].focus()
            else:
                self.open_cards[c_id] = window
                self.open_windows[window] = c_id
                window.geometry("-30+{voff}".format(voff=str(30+self.vertical_offset)))
                self.vertical_offset = (self.vertical_offset + 5) % 25
                #TODO: root logic
                card_view.CardView(card, window, self.session_factory)

    def destroyed_window(self, e):
        card = self.open_windows.pop(e.widget, "")
        self.open_cards.pop(card, None)

    def map_update(self, update_dict):
        self.tree_list.event_generate("<<TreeviewSelect>>")
