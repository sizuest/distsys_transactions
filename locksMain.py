import transaction
import threading
from wms_solution import WMS, WMSTransactions


def run_random_operations(wms: WMS, num_transactions, max_elemetns):
    wms.random_operations(num_transactions, max_elemetns)


if __name__ == '__main__':

    savepoint = transaction.savepoint()

    NUMBER_OF_TRANSACTIONS = 100
    NUMBER_OF_WAREHOUSES = 10
    NUMBER_OF_POSITIONS = 10
    NUMBER_OF_THREADS = 100

    wms_transactions = WMSTransactions(NUMBER_OF_WAREHOUSES, NUMBER_OF_POSITIONS)
    print('\n==============================================================================')
    print('SIMULATION 3: With Transaction Manager')
    print('==============================================================================\n')
    initial_content = wms_transactions.get_count()
    # Run simulation
    ops_threads = []
    for i in range(0, NUMBER_OF_THREADS):
        ops_thread = threading.Thread(target=run_random_operations, args=(wms_transactions, NUMBER_OF_TRANSACTIONS, 50))
        ops_thread.start()
        ops_threads.append(ops_thread)

    for t in ops_threads:
        t.join()

    print('\n')
    print('INITIAL CONTENT: %6.0f' % (initial_content) + '\n')
    print('FINAL CONTENT:   %6.0f' % wms_transactions.get_count())
    print('in:              %6.0f' % wms_transactions.get_incoming())
    print('out:             %6.0f' % wms_transactions.get_outgoing())
    print('-------------------------')
    print('Balance:         %6.0f' % wms_transactions.get_total_count())

    

