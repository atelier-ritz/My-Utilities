import scipy.io.wavfile
import urllib.request
import requests
import numpy as np

rawText = "最後は通して聴いてみましょう。鍵盤が手元にある人は、弾いてみたりするのもいいかもです。"
extension = "wav"
speed = 1.2


# generate audio
print("Requesting audio...")
API_ENDPOINT = "https://cloud.ai-j.jp/demo/aitalk2webapi_nop.php"
data = {"text": rawText, "speaker_id": 554, "ext": extension, "speed": speed}
response = requests.post(url=API_ENDPOINT, data=data)
if response.status_code != 200:
    print("Failed to generate the audio file. Abort the program.")

# download audio
print("Downloading audio... ")
filename = response.text.split("/")[-1]
filename = filename[: len(filename) - 3]
fileurl = "https://cloud.ai-j.jp/demo/tmp/" + filename
tmpSavePath = "./" + rawText + "." + extension
urllib.request.urlretrieve(fileurl, tmpSavePath)

# trim audio
print("Processing audio... ")
fs1, y1 = scipy.io.wavfile.read(tmpSavePath)
newWavFileAsList = y1[int(3 * fs1 / speed) :]
newWavFile = np.array(newWavFileAsList)
scipy.io.wavfile.write("./" + rawText + "." + extension, fs1, newWavFile)
