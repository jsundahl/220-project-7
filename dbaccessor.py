import sqlite3


class DBAccessor():
    def __init__(self, db_name):
        self.__conn = sqlite3.connect(db_name)

    def all_customer_report(self):
        """The list of all customers and their representatives as specified in README"""
        query = 'SELECT c.FirstName, ' \
                       'c.LastName, ' \
                       'c.Company, ' \
                       'c.Phone, ' \
                       'c.Email, ' \
                       'e.FirstName as RepFirstName, ' \
                       'e.LastName as RepLastName, ' \
                       'e.Email as RepEmail ' \
                'FROM customer c JOIN employee e ' \
                'ON c.SupportRepId = e.EmployeeId ' \
                'ORDER BY c.LastName asc'
        return self.execute_query(query)

    def all_genres(self):
        """ List of all genre names to populate the combo box as specified in README"""
        query = "SELECT Name from genre ORDER BY Name asc"
        return self.execute_query(query)

    def track_info_by_genre(self, genre):
        """ List of tracks including name, album title, artist, and unit price as specified in README"""
        query = 'SELECT t.name as TrackName, ' \
                       'al.title as AlbumTitle, ' \
                       'ar.name as ArtistName, ' \
                       't.unitPrice as UnitPrice ' \
                'FROM track t join album al ' \
                'ON t.albumId = al.albumId ' \
                'JOIN artist ar ' \
                'ON al.artistId = ar.artistId ' \
                'JOIN genre g ' \
                'ON t.GenreId = g.GenreId ' \
                'WHERE g.Name = ' + "\'{}\'".format(genre) + '' \
                'ORDER BY ar.name asc'
        return self.execute_query(query)

    def execute_query(self, query):
        cursor = self.__conn.cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        # the column headers are here:
        col_names = next(zip(*cursor.description))
        cursor.close()
        return [col_names] + result_set

# PRAGMA table_info([]);
