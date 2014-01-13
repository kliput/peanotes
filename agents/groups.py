#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

class Group:
	userList = []
	groupList = {}
	
	def __init__(self):
		self.userList = self.getUserList()
		self.groupList = self.getGroupList()
		#self.test()
		print self.userList
		print self.groupList
	
	def checkExistUser(self, name):
		exist = False
		for user in self.userList:
			if name == user:
				exist = True
		return exist

	def checkExistGroup(self, name):
		exist = False
		for key in self.groupList:
			if name == key:
				exist = True
		return exist

	def saveToFile(self, userList, groupList):
		w = open('groupList', 'w')
		for user in self.userList:
			w.write('u ' + user + '\n')
		for group in self.groupList:
			w.write('g ' + group)
			for value in self.groupList[group]:
				w.write(' '+ value)
			w.write('\n')

	def getGroupList(self):
		groupList = {}
		f = open('groupList', 'r')
		lines = f.readlines()
		for line in lines:
			if len(line)>1:
				words = line.split()
				if words[0] == "g":
					userList = []
					i = 0
					for word in words:
						i = i + 1
						if i>2:
							userList.append(word)
					groupList[words[1]] = userList
		return groupList

	def getUserList(self):
		userList = []
		f = open('groupList', 'r')
		lines = f.readlines()
		for line in lines:
			if len(line)>1:
				words = line.split()
				if words[0] == 'u':
					userList.append(words[1])
		return userList

	def addGroup(self, group, user):
		newList = []
		exist = self.checkExistGroup(group)
		exist1 = self.checkExistUser(group)
		if exist == True or exist1 == True:
			return "Podaj inna nazwe"
		else:
			newList.append(user)
			self.groupList[group] = newList
			self.saveToFile(self.userList, self.groupList)

	def addUserToGroup(self, user, group):
		exist = self.checkExistUser(group)
		exist1 = self.checkExistGroup(group)
		exist2 = self.checkExistUser(user)
		exist3 = self.checkExistGroup(user)
		if exist == False and exist1 == True and exist2 == True and exist3 == False:
			userList = self.groupList[group]
			userList.append(user)
			del self.groupList[group]
			self.groupList[group] = userList
			self.saveToFile(self.userList, self.groupList)
		else:
			return "Nie mozna dodac uzytkownika"

	def addUser(self, user):
		exist = self.checkExistUser(user)
		exist1 = self.checkExistGroup(user)
		if exist == True or exist1 == True:
			return "Taki uzytkownik juz istnieje"
		else:
			self.userList.append(user)
			self.saveToFile(self.userList, self.groupList)

	def deleteUser(self, user):
		exist = self.checkExistUser(user)
		if exist == False:
			return "Uzytkownik nie istnieje"
		else:
			self.userList.remove(user)
		for key in self.groupList:
			userList = self.groupList[key]
			if user in userList:
				userList.remove(user)
				del groupList[key]
				groupList[key] = userList
			self.saveToFile(self.userList, self.groupList)

	def deleteGroup(self, group):
		exist = self.checkExistGroup(group)
		if exist == False:
			return "Grupa nie istnieje"
		else:
			del self.groupList[group]
			self.saveToFile(self.userList, self.groupList)

	def deleteUserFromGroup(self, user, group):
		exist = self.checkExistUser(group)
		exist1 = self.checkExistGroup(group)
		exist2 = self.checkExistUser(user)
		exist3 = self.checkExistGroup(user)
		if exist == False and exist1 == True and exist2 == True and exist3 == False:
			userList = self.groupList[group]
			userList.remove(user)
			del self.groupList[group]
			self.groupList[group] = userList
			self.saveToFile(self.userList, self.groupList)
		else:
			return "Nie mozna usunac uzytkownika"
'''
	def test(self):
		self.addUser('adam')
		print self.userList
		self.addGroup('grupa_4', 'marek')
		print self.groupList
		self.addUserToGroup('piotr', 'grupa_4')
		print self.groupList
		self.addUser('john')
		print self.userList
		self.deleteUser('adam')
		print self.userList
		self.deleteUserFromGroup('marek', 'grupa_3')
		print self.groupList
		self.deleteGroup('grupa_4')
		print self.groupList
'''
if __name__ == '__main__':
	Group()

