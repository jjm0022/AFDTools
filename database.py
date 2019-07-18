import sqlite3 as lite
import re
from datetime import datetime

class DB(object):

  def __init__(self, db_path='/Users/jmiller/Dropbox/git/projects/AFDTools/forecasts.db'):
    '''
    '''
    self.db_path = db_path
    self.connection = lite.connect(self.db_path)
    self.connection.row_factory = lite.Row
    self.processed_dict = dict({'uID': 'TEXT', 'Office': 'TEXT', 'TimeStamp':'Text'})
    self.createTable('Processed', self.processed_dict)

  def execute(self, command, values=None):
    '''
    Execute the provided command
    '''
    if not values:
      with self.connection:
          cur = self.connection.cursor()
          cur.execute(command)
    else:
      with self.connection:
          cur = self.connection.cursor()
          cur.execute(command, values)

  def createTable(self, table_name, columns):
    '''
    '''
    cmd = 'CREATE TABLE IF NOT EXISTS {0} ('.format(table_name)
    for key, value in columns.items():
      cmd = cmd + '{0} {1}, '.format(key, value)
    cmd = re.sub(r'\, $', ')', cmd)
    self.execute(cmd)

  
  def insert(self, table, row_dict):
    '''
    '''
    cmd = 'INSERT INTO {0} VALUES ('.format(table)
    for key in row_dict:
      cmd = cmd + '?, '
    cmd = re.sub(r'\, $', ')', cmd)
    values = tuple(row_dict.values())
    self.execute(cmd, values) 

  def getProcessedPhrases(self, uID):
    '''
    Returns rows matching the uID from the Phrase table
    '''
    with self.connection as c:
      cur = c.cursor()
      query = cur.execute('''SELECT * FROM Phrase WHERE uID=?''', (uID,))
      rows = query.fetchall()
    for row in rows:
      yield row
    

  def updateDataset(self, uID):
    '''
    '''
    with self.connection as c:
      cur = c.cursor()
      query = cur.execute('''UPDATE Processed
                              SET Dataset=1
                              WHERE uID=?''', (uID,))


  def getUnprocessed(self):
    '''
    '''
    with self.connection as c:
      cur = c.cursor()
      query = cur.execute('''SELECT * FROM Forecast f WHERE NOT
                             EXISTS (SELECT 1 FROM Processed WHERE uID = f.uID)
                             ORDER BY Office, TimeStamp;''')
      rows = query.fetchall()
    for row in rows:
      yield row


  def getNotInDataset(self):
    '''
    '''
    with self.connection as c:
      cur = c.cursor()
      query = cur.execute('''SELECT * FROM Forecast f WHERE uID 
                             IN(SELECT uID FROM Processed WHERE Dataset = 0)
                             ORDER BY Office, TimeStamp;''')
      rows = query.fetchall()
    for row in rows:
      yield row