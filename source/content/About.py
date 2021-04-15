import tkinter as tk
import webbrowser
import source.content.GUI as GUI


class About(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.geometry("300x400")
        self.title("About")
        # self.iconbitmap("")
        self.resizable(False, False)

        self.labelsFrame = tk.Frame(self,
                                    bg=GUI.GUI.backgroundColor)
        self.labelsFrame.pack(fill=tk.BOTH, expand=True)

        self.madeBy = tk.Label(self.labelsFrame,
                               text="Made by\nKonstantin Biektin\n",
                               font="Ubuntu 12",
                               bg=GUI.GUI.backgroundColor,
                               fg=GUI.GUI.foregroundColor)
        self.madeBy.pack(fill=tk.BOTH, expand=True)

        self.contactLinksLabel = tk.Label(self.labelsFrame,
                                          text="Userful links:\n",
                                          font="Ubuntu 12",
                                          bg=GUI.GUI.backgroundColor,
                                          fg=GUI.GUI.foregroundColor)
        self.contactLinksLabel.pack(fill=tk.BOTH, side=tk.LEFT)

        self.linksFrame = tk.Frame(self,
                                   bg=GUI.GUI.backgroundColor)
        self.linksFrame.pack(fill=tk.BOTH, expand=True)

        self.img_github = tk.PhotoImage(file="../img/icons/github.png")
        self.img_github_hover = tk.PhotoImage(file="../img/icons/github(hover).png")
        self.img_twitter = tk.PhotoImage(file="../img/icons/twitter.png")
        self.img_twitter_hover = tk.PhotoImage(file="../img/icons/twitter(hover).png")
        self.img_discord = tk.PhotoImage(file="../img/icons/discord.png")
        self.img_discord_hover = tk.PhotoImage(file="../img/icons/discord(hover).png")

        self.btn_github = tk.Button(self.linksFrame,
                                    image=self.img_github,
                                    bg=GUI.GUI.backgroundColor,
                                    activebackground=GUI.GUI.backgroundColor,
                                    borderwidth=0)
        self.btn_twitter = tk.Button(self.linksFrame,
                                     image=self.img_twitter,
                                     bg=GUI.GUI.backgroundColor,
                                     activebackground=GUI.GUI.backgroundColor,
                                     borderwidth=0)
        self.btn_discord = tk.Button(self.linksFrame,
                                     image=self.img_discord,
                                     bg=GUI.GUI.backgroundColor,
                                     activebackground=GUI.GUI.backgroundColor,
                                     borderwidth=0)

        self.btn_github.grid(row=0, column=0, padx=26)
        self.btn_twitter.grid(row=0, column=1)
        self.btn_discord.grid(row=0, column=2, padx=26)

        self.githubLabel = tk.Label(self.linksFrame,
                                    text="Project\nGitHub",
                                    font="Ubuntu 12",
                                    bg=GUI.GUI.backgroundColor,
                                    fg=GUI.GUI.foregroundColor)
        self.twitterLabel = tk.Label(self.linksFrame,
                                     text="My\nTwitter",
                                     font="Ubuntu 12",
                                     bg=GUI.GUI.backgroundColor,
                                     fg=GUI.GUI.foregroundColor)
        self.discordLabel = tk.Label(self.linksFrame,
                                     text="My Discord\nServer",
                                     font="Ubuntu 12",
                                     bg=GUI.GUI.backgroundColor,
                                     fg=GUI.GUI.foregroundColor)

        self.githubLabel.grid(row=1, column=0)
        self.twitterLabel.grid(row=1, column=1)
        self.discordLabel.grid(row=1, column=2)

        self.version = tk.Label(self,
                                text="v1.0\n© 2021",
                                font="Ubuntu 10",
                                bg=GUI.GUI.backgroundColor,
                                fg=GUI.GUI.foregroundColor)
        self.version.pack(fill=tk.BOTH, expand=True)

        self.__bind_events_to_buttons()
        self.__bind_commands_to_buttons()
        self.grab_set()

    def __bind_commands_to_buttons(self):
        pass

    def __bind_events_to_buttons(self):
        self.btn_github.bind("<Enter>",
                             lambda event, image=self.img_github_hover: self.on_enter(e=event, image=image))
        self.btn_github.bind("<Leave>", lambda event, image=self.img_github: self.on_leave(e=event, image=image))
        self.btn_twitter.bind("<Enter>",
                              lambda event, image=self.img_twitter_hover: self.on_enter(e=event, image=image))
        self.btn_twitter.bind("<Leave>", lambda event, image=self.img_twitter: self.on_leave(e=event, image=image))
        self.btn_discord.bind("<Enter>",
                              lambda event, image=self.img_discord_hover: self.on_enter(e=event, image=image))
        self.btn_discord.bind("<Leave>", lambda event, image=self.img_discord: self.on_leave(e=event, image=image))

    def on_enter(self, e, image):
        e.widget['image'] = image

    def on_leave(self, e, image):
        e.widget['image'] = image
