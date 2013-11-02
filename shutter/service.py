from twisted.internet import utils, threads
import hashlib
import os

class Snapshot(object):
    def __init__(self, page):
        self._page = page
        self._file_name = ''
        self._data = ''
        self._arguments = ["-x","1920","1080", self._page]
        self._env = { 'HOME' : os.environ['HOME'] }
    def take(self):
        output = utils.getProcessOutput("/usr/local/bin/webkit2png",self._arguments, self._env)
        return output.addCallbacks(self.md5sum).addCallback(self.store)
    def md5sum(self, data):
        def _md5sum(data):
            m = hashlib.md5()
            m.update(data)
            self._file_name = "%s.png" % m.hexdigest()
            self._data = data
        return threads.deferToThread(_md5sum, data)
    def store(self, data):
        def _store(data):
            # No need to store the file if it already exists
            if not os.path.exists("static/%s" % self._file_name):
                output = open("static/%s" % self._file_name, "w")
                output.write(data)
                output.close()
            return self._file_name
        return threads.deferToThread(_store, self._data)

class Shutter(object):
    def setup_database(self, pool):
        self.__dbpool = pool
    def snapshot(self, url):
        def _save(txn, url, file_path):
            txn.execute("""SELECT id FROM shutter.urls WHERE url = %s""", [url])
            result = txn.fetchone()
            if result is None:
                txn.execute("""INSERT INTO shutter.urls(url)
                                    VALUES (%s)
                                 RETURNING id""", [url])
                result = txn.fetchone()
            url_id = result[0]
            txn.execute("""INSERT INTO shutter.snapshots(url_id, file_path)
                                VALUES (%s, %s)""", [url_id, file_path])
            return file_path
        def _store_url(file_path):
            return self.__dbpool.runInteraction(_save, url, file_path)
        return Snapshot(url).take().addCallback(_store_url)
    def snapshots(self, url):
        def _get_snapshot_urls(txn, url):
            txn.execute("""SELECT s.file_path
                             FROM shutter.urls u
                                 ,shutter.snapshots s
                            WHERE u.url = %s
                              AND u.id = s.url_id
                         ORDER BY s.created_at DESC
            """, [url])
            return [column[0] for column in txn.fetchall()]
        return self.__dbpool.runInteraction(_get_snapshot_urls, url)