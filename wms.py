import random
from warehouse import MaterialNotAvailableError, SpaceNotAvailableError, GeneralError
from warehouse import Stock, Warehouse
import transaction
from transaction.tests import savepointsample
from abc import ABC, abstractmethod


class WMS(ABC):

    def __init__(self, wh_number, pos_number):
        random.seed(0)

        self.dm = savepointsample.SampleSavepointDataManager()
        transaction.abort()
        self.dm['total_incoming'] = 0
        self.dm['total_outgoing'] = 0

        self.warehouses = self.create_warehouses(wh_number, pos_number)
        transaction.commit()

    # TRANSFER --------------------------------------------------------------------------------------------------------
    def transfer(self, source: Stock, target: Stock, amount):
        print('JOB: ' + source.get_name() + ' --(' + str(amount).zfill(3) + ')--> ' + target.get_name(), end="\t ... ")

        try:
            self.do_transfer(source, target, amount)
            print("OK")
        except (MaterialNotAvailableError, SpaceNotAvailableError, GeneralError) as error:
            print("ERROR: " + error.args[0])
        except HandledError as error:
            print("SUPPRESSED: " + error.args[0])

    @abstractmethod
    def do_transfer(self, source: Stock, target: Stock, amount):
        pass

    # FULL TRANSFER ---------------------------------------------------------------------------------------------------
    def transfer_full(self, source: Stock, target: Stock):
        self.transfer(source, target, source.get_count())

    # INCOMING --------------------------------------------------------------------------------------------------------
    def incoming(self, target: Stock, amount):
        print('JOB: 	 EXTERNAL --(' + str(amount).zfill(3) + ')--> ' + target.get_name(), end="\t ... ")

        try:
            self.dm['total_incoming'] = self.dm['total_incoming'] + amount
            self.do_incoming(target, amount)
            print("OK")
        except (MaterialNotAvailableError, SpaceNotAvailableError, GeneralError) as error:
            print("ERROR: " + error.args[0])
        except HandledError as error:
            print("SUPPRESSED: " + error.args[0])

    @abstractmethod
    def do_incoming(self, target, amount):
        pass

    # OUTGOING --------------------------------------------------------------------------------------------------------
    def outgoing(self, source: Stock, amount):
        print('JOB: ' + source.get_name() + ' --(' + str(amount).zfill(3) + ')--> EXTERNAL	 ', end="\t ... ")

        try:
            self.dm['total_outgoing'] = self.dm['total_outgoing'] + amount
            self.do_outgoing(source, amount)
            print("OK")
        except (MaterialNotAvailableError, SpaceNotAvailableError, GeneralError) as error:
            print("ERROR: " + error.args[0])
        except HandledError as error:
            print("SUPPRESSED: " + error.args[0])

    @abstractmethod
    def do_outgoing(self, source, amount):
        pass

    # WAREHOUSE -------------------------------------------------------------------------------------------------------
    def create_warehouses(self, wh_number, pos_number):
        random.seed(0)

        whs = []
        # Create warehouses
        for wh_idx in range(1, wh_number + 1):
            wh_name = 'WH-' + str(wh_idx).zfill(4)
            wh_obj = Warehouse(wh_name)
            whs.append(wh_obj)
            # Create places
            for pos_idx in range(1, pos_number + 1):
                pos_name = wh_name + '-' + str(pos_idx).zfill(4)
                wh_obj.add_stock_position(Stock(pos_name, self.dm, 150, random.randint(0, 100)))

        return whs

    # STATISTICS ------------------------------------------------------------------------------------------------------
    def get_total_count(self):
        count = self.get_count()
        count -= self.dm['total_incoming']
        count += self.dm['total_outgoing']

        return count

    def get_count(self):
        count = 0
        for pos in list(self.dm.keys()):
            count += self.dm[pos]

        count -= self.dm['total_incoming']
        count -= self.dm['total_outgoing']

        return count

    def get_outgoing(self):
        return self.dm['total_outgoing']

    def get_incoming(self):
        return self.dm['total_incoming']

    # RANDOM SELECTION OF ACTIONS -------------------------------------------------------------------------------------
    def get_random_place(self, exclude=None):
        wh = random.choice(self.warehouses)
        while wh is exclude:
            wh = random.choice(self.warehouses)

        return wh, random.choice(wh.get_positions())

    def random_transfer(self, max_count):
        src_wh, src_pos = self.get_random_place()
        trg_wh, trg_pos = self.get_random_place(src_wh)

        self.transfer(src_pos, trg_pos, random.randint(1, max_count))

    def random_transfer_full(self):
        src_wh, src_pos = self.get_random_place()
        trg_wh, trg_pos = self.get_random_place(src_wh)

        self.transfer_full(src_pos, trg_pos)

    def random_incoming(self, max_count):
        trg_wh, trg_pos = self.get_random_place()

        self.incoming(trg_pos, random.randint(1, max_count))

    def random_outgoing(self, max_count):
        src_wh, src_pos = self.get_random_place()

        self.outgoing(src_pos, random.randint(1, max_count))

    def random_operation(self, max_count):
        r = random.random()

        if r < .1:
            self.random_incoming(max_count)
        elif r < .2:
            self.random_outgoing(max_count)
        elif r < .3:
            self.random_transfer_full()
        else:
            self.random_transfer(max_count)

    def random_operations(self, num_operations, max_count):
        for i in range(0, num_operations):
            self.random_operation(max_count)


class HandledError(Exception):
    pass


# Simple WMS without transactions
class ERPSimple(WMS):

    def do_transfer(self, source: Stock, target: Stock, amount):
        # TODO: Implement functions to realize a transfer of goods
        pass

    def do_incoming(self, target, amount):
        # TODO: Implement a check-in of incoming goods
        pass

    def do_outgoing(self, source, amount):
        # TODO: Implement a check-out of outgoing goods
        pass


# Simples WMS with transactions
class ERPTransactions(WMS):
    def do_transfer(self, source: Stock, target: Stock, amount):
        try:
            # TODO: Implement functions to realize a transfer of goods and a commit of the transactions upon success
            pass
        except Exception as error:
            # TODO: Implement an abort of the transactions upon success
            raise HandledError(error.args[0])

    def do_incoming(self, target, amount):
        try:
            # TODO: Implement a check-in of incoming goods and a commit of the transactions upon success
            pass
        except Exception as error:
            # TODO: Implement an abort of the transactions upon success
            raise HandledError(error.args[0])

    def do_outgoing(self, source, amount):
        try:
            # TODO: Implement a check-out of outgoing goods and a commit of the transactions upon success
            pass
        except Exception as error:
            # TODO: Implement an abort of the transactions upon success
            raise HandledError(error.args[0])
