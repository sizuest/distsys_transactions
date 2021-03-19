import threading
import transaction

from wms import WMSTransactions, WMSTransactionsLocks

if __name__ == '__main__':

    savepoint = transaction.savepoint()

    NUMBER_OF_TRANSACTIONS = 10000
    NUMBER_OF_WAREHOUSES = 5
    NUMBER_OF_POSITIONS = 20
    NUMBER_OF_THREADS = 10

    wms_transactions = WMSTransactions(NUMBER_OF_WAREHOUSES, NUMBER_OF_POSITIONS)
    print('\n==============================================================================')
    print('SIMULATION 3: With Transaction Manager')
    print('==============================================================================\n')
    initial_content = wms_transactions.get_count()
    # Run simulation
    ops_threads = []
    for i in range(0, NUMBER_OF_THREADS):
        ops_thread = threading.Thread(target=wms_transactions.random_operations,
                                      args=(NUMBER_OF_TRANSACTIONS // NUMBER_OF_THREADS, 50))
        ops_thread.start()
        ops_threads.append(ops_thread)

    for t in ops_threads:
        t.join()

    print('INITIAL CONTENT: %6.0f' % initial_content + '\n')
    print('FINAL CONTENT:   %6.0f' % wms_transactions.get_count())
    print('in:              %6.0f' % wms_transactions.get_incoming())
    print('out:             %6.0f' % wms_transactions.get_outgoing())
    print('-------------------------')
    print('Balance:         %6.0f' % wms_transactions.get_total_count())

    exit()

    wms_transactions_locks = WMSTransactionsLocks(NUMBER_OF_WAREHOUSES, NUMBER_OF_POSITIONS)
    print('\n==============================================================================')
    print('SIMULATION 4: With Transaction Manager and Locks')
    print('==============================================================================\n')
    initial_content = wms_transactions_locks.get_count()
    # Run simulation
    ops_threads = []
    for i in range(0, NUMBER_OF_THREADS):
        ops_thread = threading.Thread(target=wms_transactions_locks.random_operations,
                                      args=(NUMBER_OF_TRANSACTIONS // NUMBER_OF_THREADS, 50))
        ops_thread.start()
        ops_threads.append(ops_thread)

    for t in ops_threads:
        t.join()

    print('INITIAL CONTENT: %6.0f' % initial_content + '\n')
    print('FINAL CONTENT:   %6.0f' % wms_transactions_locks.get_count())
    print('in:              %6.0f' % wms_transactions_locks.get_incoming())
    print('out:             %6.0f' % wms_transactions_locks.get_outgoing())
    print('-------------------------')
    print('Balance:         %6.0f' % wms_transactions_locks.get_total_count())
