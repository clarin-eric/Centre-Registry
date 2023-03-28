import json
from json import JSONDecoder, JSONEncoder
from
from typing import Generic, Iterable, List, Protocol, Type, TypeVar


class ProtocolT(Protocol):
    def __init__(self, *args, **kwargs):
        pass


    def __str__(self):
        pass


TypeT = TypeVar('TypeT', bound=ProtocolT)


class DjangoArrayDecodingException(Exception):
    """
        Exception raised inside djangoarrayfield.DjangoArrayDecoder
    """
    def __init__(self, obj: object, message: str= None,  _type: Type = TypeT):
        if message is None:
            self.message: str = f"Error when decoding array of {TypeT} object's\n{obj}"
        else:
            self.message = message
        self._type: TypeT = TypeT
        super().__init__(self.message)


class DjangoArrayEncodingException(Exception):
    """
        Exception raised inside djangoarrayfield.DjangoArrayEncoder
    """
    def __init__(self, obj: object, message: str, _type: Type = TypeT):
        if message is None:
            self.message: str = f"Error when encoding array of {TypeT} object's\n{obj}"
        else:
            self.message: str = message
        self._type: TypeT = TypeT
        super().__init__(self.message)


class DjangoArrayDecoder(Generic[TypeT], JSONDecoder):
    """
        Generic array decoder for Django, built on top of json.JSONDecoder
    """

    def default(self, obj: Iterable[TypeT]):
        """
            Returns deserialized array of objects of generic type TypeT
        """
        try:
            ret: List[TypeT] = [TypeT.__init__(o) for o in obj]
        except Exception as e:
            raise DjangoArrayDecodingException(obj=obj, _type=TypeT)
        return JSONDecoder.decode(self, ret)

class DjangoArrayEncoder(Generic[TypeT], JSONEncoder):
    """
        Generic array encoder for Django, built on top of json.JSONEncoder
    """
    def default(self, obj: Iterable[TypeT]):
        """
            Return serializable representation of an array of objects of generic type TypeT
        """
        try:
            ret: List[str] = [str(o) for o in obj]
        except:
            raise DjangoArrayEncodingException(obj=obj, _type=TypeT)
        return JSONEncoder.default(self, ret)
