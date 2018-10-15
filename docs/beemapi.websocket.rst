dpaycliapi\.websocket
==================

This class allows subscribe to push notifications from the DPay
node.

.. code-block:: python

    from pprint import pprint
    from dpaycliapi.websocket import DPayWebsocket

    ws = DPayWebsocket(
        "wss://gtg.dpay.house:8090",
        accounts=["test"],
        on_block=print,
    )

    ws.run_forever()


.. autoclass:: dpaycliapi.websocket.DPayWebsocket
    :members:
    :undoc-members:
    :private-members:
    :special-members:


