import transaction
from wms import ERPSimple, ERPTransactions

from transaction.tests import savepointsample


if __name__ == '__main__':

    savepoint = transaction.savepoint()

    NUMBER_OF_TRANSACTIONS = 100
    NUMBER_OF_WAREHOUSES = 10
    NUMBER_OF_POSITIONS = 100

    wmssimple = ERPSimple(NUMBER_OF_WAREHOUSES, NUMBER_OF_POSITIONS)
    print('\n==============================================================================')
    print('SIMULATION 1: No Transaction Manager')
    print('==============================================================================\n')
    print('INITIAL CONTENT: ' + str(wmssimple.get_count()) + '\n')
    # Run simulation
    wmssimple.random_operations(NUMBER_OF_TRANSACTIONS, 15)
    print('\nFINAL CONTENT: %6.0f' % wmssimple.get_count())
    print('in:            %6.0f' % wmssimple.get_incoming())
    print('out:           %6.0f' % wmssimple.get_outgoing())
    print('-------------------------')
    print('Balance:       %6.0f' % wmssimple.get_total_count())

    wmstransactions = ERPTransactions(NUMBER_OF_WAREHOUSES, NUMBER_OF_POSITIONS)
    print('\n==============================================================================')
    print('SIMULATION 2: With Transaction Manager')
    print('==============================================================================\n')
    print('INITIAL CONTENT: ' + str(wmssimple.get_count()) + '\n')
    # Run simulation
    wmstransactions.random_operations(NUMBER_OF_TRANSACTIONS, 15)
    print('\nFINAL CONTENT: %6.0f' % wmstransactions.get_count())
    print('in:            %6.0f' % wmstransactions.get_incoming())
    print('out:           %6.0f' % wmstransactions.get_outgoing())
    print('-------------------------')
    print('Balance:       %6.0f' % wmstransactions.get_total_count())
