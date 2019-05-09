from honeybadgermpc.config import HbmpcConfig
from honeybadgermpc.ipc import ProcessProgramRunner
from honeybadgermpc.poly_commit_const import gen_pc_const_crs
from honeybadgermpc.hbavss import get_avss_params, HbAvssBatch
from honeybadgermpc.betterpairing import ZR
import asyncio
import time
import logging

#logger = logging.getLogger(__name__)
#logger.setLevel(logging.ERROR)
# Uncomment this when you want logs from this file.
#logger.setLevel(logging.NOTSET)

async def test():
    n = 16
    t = (n-1)//3
    batch_size = 100
    g, h, pks, sks = get_avss_params(n + 1, t)
    crs = gen_pc_const_crs(t, g=g, h=h)
    values = None
    dealer_id = n
    values = [ZR.random(0)] * batch_size
    my_id = dealer_id
    print('dealer message', 'n:', n, 'k:', batch_size)
    with HbAvssBatch(pks, sks[my_id], crs, n, t, my_id, None, None) as hbavss:
        m1,m2 = hbavss._get_dealer_msg(values, n)
        print('len(commitents):', len(m1))
        print('map(dispersal_msg_list):', list(map(len,m2)))

if __name__ == '__main__':
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(test())
    finally:
        loop.close()
