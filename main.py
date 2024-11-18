import sys
import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import os

class Strick_Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Strick Browser")
        self.setGeometry(400, 150, 1200, 800)
        self.setWindowIcon(QIcon("Stricks-Browser-logo.png"))
        self.setStyleSheet(self.get_dark_theme())

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.tabBarDoubleClicked.connect(self.add_new_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.setCentralWidget(self.tabs)

        nav_bar = QToolBar()
        nav_bar.setIconSize(QSize(32, 32))
        nav_bar.setMovable(False)
        self.addToolBar(nav_bar)

        self.icons = {
            "back": self.get_icon("https://img.icons8.com/?size=100&id=108810&format=png&color=FFFFFF"),
            "forward": self.get_icon("https://img.icons8.com/?size=100&id=110230&format=png&color=FFFFFF"),
            "reload": self.get_icon("https://img.icons8.com/?size=100&id=115634&format=png&color=FFFFFF"),
            "home": self.get_icon("https://img.icons8.com/?size=100&id=12847&format=png&color=FFFFFF"),
            "new_tab": self.get_icon("https://img.icons8.com/?size=100&id=aWZy3jlAFSa9&format=png&color=FFFFFF"),
            "bookmark": self.get_icon("https://img.icons8.com/?size=100&id=102717&format=png&color=FFFFFF"),
            "View-Bookmarks": self.get_icon("https://img.icons8.com/?size=100&id=102713&format=png&color=FFFFFF"),
        }

        back_btn = QAction(QIcon(self.icons["back"]), "Back", self)
        back_btn.triggered.connect(self.navigate_back)
        nav_bar.addAction(back_btn)

        forward_btn = QAction(QIcon(self.icons["forward"]), "Forward", self)
        forward_btn.triggered.connect(self.navigate_forward)
        nav_bar.addAction(forward_btn)

        reload_btn = QAction(QIcon(self.icons["reload"]), "Reload", self)
        reload_btn.triggered.connect(self.reload_page)
        nav_bar.addAction(reload_btn)

        home_btn = QAction(QIcon(self.icons["home"]), "Home", self)
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet("color: white; background-color: #333; border-radius: 10px; padding: 10px; font-size: 16px;")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        go_btn = QPushButton("Go")
        go_btn.setStyleSheet("font-size: 16px; padding: 10px;")  
        go_btn.clicked.connect(self.navigate_to_url)
        nav_bar.addWidget(go_btn)

        new_tab_btn = QAction(QIcon(self.icons["new_tab"]), "New Tab", self)
        new_tab_btn.triggered.connect(self.add_new_tab)
        nav_bar.addAction(new_tab_btn)

        self.add_new_tab(QUrl("https://www.google.com"), "New Tab")

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        self.bookmarks = []
        bookmark_btn = QAction(QIcon(self.icons["bookmark"]), "Bookmark", self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        nav_bar.addAction(bookmark_btn)
        
        view_bookmarks_btn = QAction(QIcon(self.icons["View-Bookmarks"]), "View-Bookmarks", self)
        view_bookmarks_btn.triggered.connect(self.view_bookmarks)
        nav_bar.addAction(view_bookmarks_btn)
        
    def add_bookmark(self):
        current_url = self.tabs.currentWidget().url().toString()
        if current_url not in self.bookmarks:
            self.bookmarks.append(current_url)
            QMessageBox.information(self, "Bookmark Added", f"'{current_url}' has been added to bookmarks.")
        else:
            QMessageBox.warning(self, "Bookmark Exists", f"'{current_url}' is already in your bookmarks.")

    def view_bookmarks(self):
        if not self.bookmarks:
            QMessageBox.information(self, "No Bookmarks", "You have no bookmarks.")
            return

        bookmarks_dialog = QDialog(self)
        bookmarks_dialog.setWindowTitle("Bookmarks")
        bookmarks_dialog.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        bookmarks_list = QListWidget()
        bookmarks_list.addItems(self.bookmarks)
        bookmarks_list.itemDoubleClicked.connect(self.open_bookmark)
        layout.addWidget(bookmarks_list)

        bookmarks_dialog.setLayout(layout)
        bookmarks_dialog.exec_()

    def open_bookmark(self, item):
        url = item.text()
        self.add_new_tab(QUrl(url), "Bookmark")

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl("http://www.google.com")
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(self.update_url_bar)
        browser.loadFinished.connect(lambda _, i=i: self.tabs.setTabText(i, browser.page().title()))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

    def get_icon(self, url):
        response = requests.get(url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        return pixmap

    def get_dark_theme(self):
        return """
        QMainWindow {
            background-color: #1e1e1e;  /* Fixed color code */
            color: white;
        }
        QToolBar {
            background-color: #2e2e2e;
            border: none;
        }
        QTabBar::tab {
            background: #2e2e2e;
            color: white;
            padding: 10px;
            border: 1px solid #444;
            border-bottom: none;
        }
        QTabBar::tab:selected {
            background: #444;
        }
        QLineEdit {
            border: 1px solid #444;
            border-radius: 5px;
        }
        QPushButton {
            background-color: #444;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #555;
        }
        QStatusBar {
            background-color: #2e2e2e;
            color: white;
        }
        """

    def add_new_tab(self, url=None, label="New Tab"):
        if url is None:
            url = QUrl("http://www.google.com")
        browser = QWebEngineView()
        browser.setUrl(url)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url_bar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i: self.tabs.setTabText(i, browser.page().title()))

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def navigate_back(self):
        current_browser = self.current_browser()
        if current_browser:
            current_browser.back()

    def navigate_forward(self):
        current_browser = self.current_browser()
        if current_browser:
            current_browser.forward()

    def reload_page(self):
        current_browser = self.current_browser()
        if current_browser:
            current_browser.reload()

    def navigate_home(self):
        home_page_path = os.path.join(os.path.dirname(__file__), 'home.html')
        self.add_new_tab(QUrl.fromLocalFile(home_page_path), "Home")

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.current_browser().setUrl(q)

    def current_browser(self):
        return self.tabs.currentWidget()

    def update_url_bar(self, q, browser):
        if browser == self.current_browser():
            self.url_bar.setText(q.toString())
            self.url_bar.setCursorPosition(0)

    def tab_changed(self, i):
        if i >= 0:
            self.update_url_bar(self.current_browser().url(), self.current_browser())
            self.statusBar().showMessage("Loaded: " + self.current_browser().url().toString(), 5000)  # Use self.statusBar()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Strick_Browser()
    window.show()
    sys.exit(app.exec_())