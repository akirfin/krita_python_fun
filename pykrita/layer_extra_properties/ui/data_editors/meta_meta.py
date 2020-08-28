from abc import ABCMeta
from PyQt5.QtCore import QObject


class MetaMeta(type(QObject), ABCMeta):
    """
    Too meta for me, so thats why the name!
    (Nothing to see, move along...)

    Union of Shiboken.ObjectType & ABCmeta metaclasses.
    Allows use of collections.abc interfaces with QObjects.
    """
