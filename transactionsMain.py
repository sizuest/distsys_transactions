import transaction
from transaction.tests import savepointsample
import warehouse
import random


def transfer(source: warehouse.Stock, target: warehouse.Stock, amount):
    print('JOB: ' + source.get_name() + ' --(' + str(amount).zfill(3) + ')--> ' + target.get_name(), end="\t ... ")
    target.put(amount)
    source.pick(amount)


def transfer_full(source: warehouse.Stock, target: warehouse.Stock):
    transfer(source, target, source.get_count())


def incoming(target: warehouse.Stock, amount):
    print('JOB: 	 EXTERNAL --(' + str(amount).zfill(3) + ')--> ' + target.get_name(), end="\t ... ")
    dm['total_incoming'] = dm['total_incoming'] + amount
    target.put(amount)


def outgoing(source: warehouse.Stock, amount):
    print('JOB: ' + source.get_name() + ' --(' + str(amount).zfill(3) + ')--> EXTERNAL	 ', end="\t ... ")
    dm['total_outgoing'] = dm['total_outgoing'] + amount
    source.pick(amount)


def create_warehouses(wh_number, pos_number):
    whs = []
    # Create warehouses
    for wh_idx in range(1, wh_number+1):
        wh_name = 'WH-'+str(wh_idx).zfill(4)
        wh_obj = warehouse.Warehouse(wh_name)
        whs.append(wh_obj)
        # Create places
        for pos_idx in range(1, pos_number+1):
            pos_name = wh_name+'-'+str(pos_idx).zfill(4)
            wh_obj.add_stock_position(warehouse.Stock(pos_name, dm, 150, random.randint(0, 100)))

    return whs


def random_transfer(max_count):
    src_wh, src_pos = get_random_place()
    trg_wh, trg_pos = get_random_place(src_wh)

    transfer(src_pos, trg_pos, random.randint(1, max_count))


def random_transfer_full():
        src_wh, src_pos = get_random_place()
        trg_wh, trg_pos = get_random_place(src_wh)

        transfer_full(src_pos, trg_pos)


def random_incoming(max_count):
    trg_wh, trg_pos = get_random_place()

    incoming(trg_pos, random.randint(1, max_count))


def random_outgoing(max_count):
    src_wh, src_pos = get_random_place()

    outgoing(src_pos, random.randint(1, max_count))


def random_operation(max_count):
    r = random.random()

    if r < .1:
        random_incoming(max_count)
    elif r < .2:
        random_outgoing(max_count)
    elif r < .3:
        random_transfer_full()
    else:
        random_transfer(max_count)


def random_operations(count, max_amount, use_tm=False):
    for i in range(0, count):
        try:
            random_operation(max_amount)
            print("OK")
            if use_tm:
                transaction.commit()
        except:
            print("FEHLER")
            if use_tm:
                transaction.abort()


def get_random_place(exclude=None):
    wh = random.choice(warehouses)
    while wh is exclude:
        wh = random.choice(warehouses)

    return wh, random.choice(wh.get_positions())


def get_total_count():
    count = 0
    for pos in list(dm.keys()):
        count += dm[pos]

    count -= dm['total_incoming']
    count -= dm['total_outgoing']

    return count


def init_simulation():
    random.seed(0)

    global savepoint
    savepoint.rollback()


if __name__ == '__main__':

    dm = savepointsample.SampleSavepointDataManager()
    dm['total_incoming'] = 0
    dm['total_outgoing'] = 0
    warehouses = create_warehouses(5, 100)
    transaction.commit()
    savepoint = transaction.savepoint()

    NUMBER_OF_TRANSACTIONS = 10

    print('\n==============================================================================')
    print('SIMULATION 1: No Transaction Manager')
    print('==============================================================================\n')
    init_simulation()
    print('INITIAL CONTENT: ' + str(get_total_count()) + '\n')
    # Run simulation
    random_operations(NUMBER_OF_TRANSACTIONS, 75)
    print('\nFINAL CONTENT: %6.0f' % get_total_count())
    print('in:            %6.0f' % dm['total_incoming'])
    print('out:           %6.0f' % dm['total_outgoing'])
    print('-------------------------')
    print('TOTAL:         %6.0f' % (get_total_count() - dm['total_incoming'] + dm['total_outgoing']))

    print('\n==============================================================================')
    print('SIMULATION 2: With Transaction Manager')
    print('==============================================================================\n')
    init_simulation()
    print('INITIAL CONTENT: ' + str(get_total_count()) + '\n')
    # Run simulation
    random_operations(NUMBER_OF_TRANSACTIONS, 75, True)
    print('\nFINAL CONTENT: %6.0f' % get_total_count())
    print('in:            %6.0f' % dm['total_incoming'])
    print('out:           %6.0f' % dm['total_outgoing'])
    print('-------------------------')
    print('TOTAL:         %6.0f' % (get_total_count() - dm['total_incoming'] + dm['total_outgoing']))
