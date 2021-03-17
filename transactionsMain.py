import transaction
from wms import WMSSimple, WMSTransactions

if __name__ == '__main__':

    savepoint = transaction.savepoint()

    NUMBER_OF_TRANSACTIONS = 100
    NUMBER_OF_WAREHOUSES = 10
    NUMBER_OF_POSITIONS = 100

    wms_simple = WMSSimple(NUMBER_OF_WAREHOUSES, NUMBER_OF_POSITIONS)
    print('\n==============================================================================')
    print('SIMULATION 1: No Transaction Manager')
    print('==============================================================================\n')
    initial_content = wms_simple.get_count()
    # Run simulation
    wms_simple.random_operations(NUMBER_OF_TRANSACTIONS, 50)
    print('\n')
    print('INITIAL CONTENT: %6.0f' % (initial_content) + '\n')
    print('FINAL CONTENT:   %6.0f' % wms_simple.get_count())
    print('in:              %6.0f' % wms_simple.get_incoming())
    print('out:             %6.0f' % wms_simple.get_outgoing())
    print('-------------------------')
    print('Balance:         %6.0f' % wms_simple.get_total_count())

    wms_transactions = WMSTransactions(NUMBER_OF_WAREHOUSES, NUMBER_OF_POSITIONS)
    print('\n==============================================================================')
    print('SIMULATION 2: With Transaction Manager')
    print('==============================================================================\n')
    initial_content = wms_transactions.get_count()
    # Run simulation
    wms_transactions.random_operations(NUMBER_OF_TRANSACTIONS, 50)
    print('\n')
    print('INITIAL CONTENT: %6.0f' % (initial_content) + '\n')
    print('FINAL CONTENT:   %6.0f' % wms_transactions.get_count())
    print('in:              %6.0f' % wms_transactions.get_incoming())
    print('out:             %6.0f' % wms_transactions.get_outgoing())
    print('-------------------------')
    print('Balance:         %6.0f' % wms_transactions.get_total_count())



