class Shutter(object):
    def setup_database(self, pool):
        self.__dbpool = pool
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