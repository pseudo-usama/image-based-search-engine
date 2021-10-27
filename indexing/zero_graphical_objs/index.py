from math import ceil

from ..index_for import IndexFor

from DB.schema import *


def index_data(BBs, imgName, indexFor):
    if indexFor == IndexFor.onlySubmit:
        return index_for_submit(BBs, imgName)

    elif indexFor == IndexFor.bothSubmitSearch:
        indexedForSubmit = index_for_submit(BBs, imgName)
        dataForSearch = index_for_search(BBs)

        return indexedForSubmit, dataForSearch


def index_for_submit(BBs, imgName):
    return {
        f'0.{len(BBs["SBBs"])}.{len(BBs["DBBs"])}': {
            'SBBs': BBs['SBBs'],
            'DBBs': BBs['DBBs'],
            'img': imgName
        }
    }


def index_for_search(BBs):
    noOfSBBs = str(len(BBs["SBBs"]))
    noOfDBBs = str(len(BBs["DBBs"]))

    query = {
        '_id': 1,
        f'0.{noOfSBBs}.{noOfDBBs}': {
            '$elemMatch': {
                'SBBs': BBs['SBBs']
            }
        }
    }

    filterFields = {
        '_id': 0,
        f'0.{noOfSBBs}.{noOfDBBs}': {
            'DBBs': 1,
            'img': 1
        }
    }

    def retriveData(obj):
        return obj\
            .get('0', {})\
            .get(noOfSBBs, {})\
            .get(noOfDBBs, None)

    return {
        'query': query,
        'filterFields': filterFields,
        'retriveData': retriveData
    }
