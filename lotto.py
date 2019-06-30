#!/usr/bin/python3

import os
import requests
from bs4 import BeautifulSoup

def checkJoker(ourRows, correctRow):
  rowCount = 0
  result = {}

  for row in ourRows:
    rowCount += 1
    # Check for all seven correct numbers
    if((row[0] == correctRow[0]) and
       (row[1] == correctRow[1]) and
       (row[2] == correctRow[2]) and
       (row[3] == correctRow[3]) and
       (row[4] == correctRow[4]) and
       (row[5] == correctRow[5]) and
       (row[6] == correctRow[6])):
  
      result[rowCount] = (7, 10000000)
      continue

    # Check for six correct numbers, beginning or end
    elif(((row[0] == correctRow[0]) and
           (row[1] == correctRow[1]) and
           (row[2] == correctRow[2]) and
           (row[3] == correctRow[3]) and
           (row[4] == correctRow[4]) and
           (row[5] == correctRow[5])) or
          ((row[1] == correctRow[1]) and
           (row[2] == correctRow[2]) and
           (row[3] == correctRow[3]) and
           (row[4] == correctRow[4]) and
           (row[5] == correctRow[5]) and
           (row[6] == correctRow[6]))):

      result[rowCount] = (6, 250000)
      continue
  
    # Check for five correct numbers, beginning or end
    elif(((row[0] == correctRow[0]) and
           (row[1] == correctRow[1]) and
           (row[2] == correctRow[2]) and
           (row[3] == correctRow[3]) and
           (row[4] == correctRow[4])) or
          ((row[2] == correctRow[2]) and
           (row[3] == correctRow[3]) and
           (row[4] == correctRow[4]) and
           (row[5] == correctRow[5]) and
           (row[6] == correctRow[6]))):

      result[rowCount] = (5, 20000)
      continue

    # Check for four correct numbers, beginning or end
    elif(((row[0] == correctRow[0]) and
           (row[1] == correctRow[1]) and
           (row[2] == correctRow[2]) and
           (row[3] == correctRow[3])) or
          ((row[3] == correctRow[3]) and
           (row[4] == correctRow[4]) and
           (row[5] == correctRow[5]) and
           (row[6] == correctRow[6]))):

      result[rowCount] = (4, 2000)
      continue

    # Check for three correct numbers, beginning or end
    elif(((row[0] == correctRow[0]) and
           (row[1] == correctRow[1]) and
           (row[2] == correctRow[2])) or
          ((row[4] == correctRow[4]) and
           (row[5] == correctRow[5]) and
           (row[6] == correctRow[6]))):

      result[rowCount] = (3, 200)
      continue

    # Check for two correct numbers, beginning or end
    elif(((row[0] == correctRow[0]) and
           (row[1] == correctRow[1])) or
          ((row[5] == correctRow[5]) and
           (row[6] == correctRow[6]))):

      result[rowCount] = (2, 80)
      continue

    else:
      result[rowCount] = (0, 0)

  return result
# End of checkJoker

my_url='https://www.texttvresultat.se/590-lotto-resultat/'

page = requests.get(my_url)
soup = BeautifulSoup(page.text, 'html.parser')

lottowrappers = soup.find_all(class_='lottowrapper')
lottoaddwrappers = soup.find_all(class_='lottoaddwrapper')
payoutwrappers = soup.find_all(class_='payout')
jokerwrappers = soup.find_all(class_='jokerwrapper')

def collectCorrectRow(wrapper):
  result = []
  numbers = wrapper.find_all(class_='number')
  for num in numbers:
    result.append(num.text)
  return result

def getPayouts(table):
  result = {}
  data = []

  rows = table.find_all('tr')
  for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # Get rid of empty values
  
  for d in data:
    if d and 'rätt' in d[0]:
      result[d[0].split(' ', 1)[0]] = d[2]
  
  return result

# Lotto1 hides in 1st instance of class lottowrappers
lotto1 = collectCorrectRow(lottowrappers[0])
# Lotto1 additional numbers hides in 1st instance of class lottoaddwrapper
lotto1add = collectCorrectRow(lottoaddwrappers[0])
# Lotto2 hides in 2nd instance of class lottowrapper
lotto2 = collectCorrectRow(lottowrappers[1])
# Lotto2 additional numbers hides in 2nd instance of class lottoaddwrapper
lotto2add = collectCorrectRow(lottoaddwrappers[1])
# Joker hides in first and only instance of class jokerwrapper
joker = collectCorrectRow(jokerwrappers[0])
# Payout table for Lotto1 resides in 1st payoutwrapper
payings1 = getPayouts(payoutwrappers[0])
# Payout table for Lotto2 resides in 2nd payoutwrapper
payings2 = getPayouts(payoutwrappers[1])

pathToLottoRows = os.path.join(os.getcwd(), 'lottorader.txt')
lottoRows = []
# open our lotto rows
with open(pathToLottoRows, 'r') as f:
  line = f.readline()
  while line:
    lottoRows.append(line.strip().split('-'))
    line = f.readline()

pathToJokerRows = os.path.join(os.getcwd(), 'jokerrader.txt')
jokerRows = []
# open our lotto rows
with open(pathToJokerRows, 'r') as f:
  line = f.readline()
  while line:
    jokerRows.append(line.strip().split('-'))
    line = f.readline()

# Rätta raderna
# Go through our rows and see how many that are correct.
listCount = 0
Lotto1Result = {}
Lotto2Result = {}
for list in lottoRows:
  listCount+=1
  hitcountLotto1 = 0
  hitcountTillagg1 = 0
  hitcountLotto2 = 0
  hitcountTillagg2 = 0
  for number in list:
    if number in lotto1:
      hitcountLotto1 +=1

    if number in lotto1add:
      hitcountTillagg1 += 1
    Lotto1Result[listCount] = (hitcountLotto1, hitcountTillagg1)

    if number in lotto2:
      hitcountLotto2 +=1
    if number in lotto2add:
      hitcountTillagg2 += 1
    Lotto2Result[listCount] = (hitcountLotto2, hitcountTillagg2)

# Check joker 
jokerResult = checkJoker(jokerRows, joker)

# Compile the SMS
print('Här kommer resultatet')
print('---------------------')
# Lotto1
wincount = 0
for rad, hits in Lotto1Result.items():
  if hits[0] > 3:
    wincount += 1
    key = str(hits[0])
    print('Vi vann på Lotto1! Rad {}, Antal rätt {}, Tillägg {}, vilket ger {}'.format(rad, hits[0], hits[1], payings1[key]))

if wincount == 0:
  print('Ingen vinst på lotto1, pisspotta!')  

# Lotto2
print('---------------------')
wincount = 0
for rad, hits in Lotto2Result.items():
  if hits[0] > 3:
    wincount += 1
    key = str(hits[0])
    print('Vi vann på Lotto2! Rad {}, Antal rätt {}, Tillägg {}, vilket ger {}'.format(rad, hits[0], hits[1], payings2[key]))

if wincount == 0:
  print('Ingen vinst på lotto2, pisspotta!')

# Jokern
print('---------------------')
wincount = 0
for rad, hits in jokerResult.items():
  if hits[0] > 1:
    wincount += 1
    key = str(hits[0])
    print('Vi vann på Jokern! Rad {}, Antal rätt {}, vilket ger {}'.format(rad, hits[0], hits[1]))

if wincount == 0:
  print('Ingen vinst på Jokern, pisspotta!') 

print('---------------------')
print('Med reservation för eventuella tryckfel och buggar')
print('')
print('Created by Jonilma AB\n')