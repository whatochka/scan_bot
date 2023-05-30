import sqlite3


class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id, lang):
        result = self.cursor.execute("SELECT `ID` FROM `users` WHERE `user_id`=? AND `lang` = ?", (user_id, lang))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT `ID` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id, lang):
        self.cursor.execute("INSERT INTO `users` (`user_id`,`lang`) VALUES (?,?)", (user_id, lang))
        return self.conn.commit()

    def add_record(self, user_id, words):
        self.cursor.execute("INSERT INTO `records` (`users_id`,`words`) VALUES (?,?)",
                            (self.get_user_id(user_id), words))
        return self.conn.commit()

    def del_dict(self, user_id, words):
        self.cursor.execute("DELETE FROM `records` WHERE `words` = ?", (words,))
        return self.conn.commit()

    def add_records(self, user_id, within="*"):
        if within == 'day':
            result = self.cursor.execute(
                "SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now','start of day') "
                "AND datetime('now','localtime') ORDER BY `date`",
                (self.get_user_id(user_id),))

        elif within == 'month':
            result = self.cursor.execute(
                "SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now','-6 days') "
                "AND datetime('now','localtime') ORDER BY `date`",
                (self.get_user_id(user_id),))

        elif within == 'year':
            result = self.cursor.execute(
                "SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now','start of month') "
                "AND datetime('now','localtime') ORDER BY `date`",
                (self.get_user_id(user_id),))

        else:
            result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? ORDER BY `date`",
                                         (self.get_user_id(user_id),))
        return result.fetchall()

    def take_rec(self, user_id):
        result = self.cursor.execute("SELECT `words` FROM `records` WHERE `users_id` = ?", (self.get_user_id(user_id),))
        return result.fetchall()

    def close(self):
        self.conn.close()
