import json
import os
import MarkovMapperV1 as mappy

# Difficulty names and ranks recognized by Beat Saber
POSSIBLE_DIFF_NAMES = ['Easy', 'Normal', 'Hard', 'Expert', 'ExpertPlus']
DIFFICULTY_RANKS = {
    'Easy': 1,
    'Normal': 3,
    'Hard': 5,
    'Expert': 7,
    'ExpertPlus': 9
}

# puts the song information (artist, name, bpm, etc.) into a dictionary to be put into info.dat
def createInfoDict(songInfo, mapInfo, customSongData=None):
    info = {
        '_version': '2.0.0',
        '_songName': songInfo['name'],
        '_songSubName': songInfo['subName'],
        '_songAuthorName': songInfo['artist'],
        '_levelAuthorName': 'AutoBeat',
        '_beatsPerMinute': songInfo['bpm'],
        '_shuffle': 0,
        '_shufflePeriod': 0.5,
        '_previewStartTime': mapInfo['pStart'],
        '_previewDuration': mapInfo['pDur'],
        '_songFilename': songInfo['audio'],
        '_coverImageFilename': songInfo['cover'],
        '_environmentName': mapInfo['env'],
        '_allDirectionsEnvironmentName': 'GlassDesertEnvironment',
        '_songTimeOffset': 0,
        '_difficultyBeatmapSets': []
    }
    if customSongData is not None:
        info['_customData'] = customSongData
    return info


# Creates an empty map of the specified difficulty to be mapped into
def createDifficulty(songFolderName, diff, style):
    diff_dict = {
        '_version': '2.0.0',
        # '_customData': {

        # }
        '_notes': [],
        '_events': []
    }
    f = open(songFolderName + '\\' + diff + style + '.dat', 'w')
    json.dump(diff_dict, f)
    f.close()


# updates an existing difficulty or creates a new one if specified difficulty does not exist
def updateDifficulty(info, diffInfo, customData=None):
    difficultyJSON = {
        "_difficulty": diffInfo['diff'],
        "_difficultyRank": DIFFICULTY_RANKS[diffInfo['diff']],
        "_beatmapFilename": diffInfo['diff'] + diffInfo['type'] + '.dat',
        "_noteJumpMovementSpeed": diffInfo['njs'],
        "_noteJumpStartBeatOffset": diffInfo['offset']
    }

    setJSON = {
        '_beatmapCharacteristicName': 'Standard',
        '_difficultyBeatmaps': []
    }

    if customData is not None:
        difficultyJSON['_customData'] = customData

    setIndex = len(info['_difficultyBeatmapSets'])
    for s in range(len(info['_difficultyBeatmapSets'])):
        if info['_difficultyBeatmapSets'][s]['_beatmapCharacteristicName'] == diffInfo['type']:
            setIndex = s
            break
    if setIndex == len(info['_difficultyBeatmapSets']):
        info['_difficultyBeatmapSets'].append(setJSON)

    for d in range(len(info['_difficultyBeatmapSets'][setIndex]['_difficultyBeatmaps'])):
        if info['_difficultyBeatmapSets'][setIndex]['_difficultyBeatmaps'][d]['_difficultyRank'] > DIFFICULTY_RANKS[diffInfo['diff']]:
            info['_difficultyBeatmapSets'][setIndex]['_difficultyBeatmaps'].insert(d, difficultyJSON)
            return
        elif info['_difficultyBeatmapSets'][setIndex]['_difficultyBeatmaps'][d]['_difficultyRank'] == DIFFICULTY_RANKS[diffInfo['diff']]:
            info['_difficultyBeatmapSets'][setIndex]['_difficultyBeatmaps'][d] = difficultyJSON
            return
    info['_difficultyBeatmapSets'][setIndex]['_difficultyBeatmaps'].append(difficultyJSON)


# dumps the info dictionary into a dat file that Beat Saber can understand
def createInfoDat(info, songFolderName):
    infoJSON = json.dumps(info, indent=2)
    f = open(songFolderName+'\\Info.dat', 'w')
    f.write(infoJSON)
    f.close()


# creates the folder the final map and info.dat are exported into
def createSongFolder(songFolderName):
    if not os.path.exists(songFolderName):
        os.mkdir(songFolderName)


# main function that when run creates a map (currently mapping Look What You Made Me Do - Taylor Swift)
def createTestFolder():
    createSongFolder('test')
    songInfo = {
        'name': 'Markov',
        'subName': '',
        'artist': 'w/e',
        'bpm': 128,
        'audio': 'song.ogg',
        'cover': ''
    }
    mapInfo = {
        'pStart': 1,
        'pDur': 10,
        'env': 'DefaultEnvironment',
    }
    infoDict = createInfoDict(songInfo, mapInfo)

    eplusInfo = {
        'type': 'Standard',
        'diff': 'ExpertPlus',
        'njs': 20,
        'offset': .067
    }

    updateDifficulty(infoDict, eplusInfo)
    createInfoDat(infoDict, 'test')
    createDifficulty('test', 'ExpertPlus', 'Standard')


createTestFolder()
mappy.mapDifficulty('test', 'ExpertPlus', 'Standard')
