import transaction
from transaction.tests import savepointsample

dm = savepointsample.SampleSavepointDataManager()

dm['a'] = 3
dm['b'] = "Test"
transaction.commit()
print("Initial: " + str(dm))

dm['a'] = 5
print("Nach Änderung: " + str(dm))
transaction.abort()
print("Nach Abort: " + str(dm))

dm['a'] = 5
print("Nach Änderung: " + str(dm))
transaction.commit()
print("Nach Commit: " + str(dm))
