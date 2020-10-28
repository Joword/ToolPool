# -*- coding:utf-8 -*-
#@Time : 2020/10/22 0022 10:19
#@Author: Joword
#@File : Sort.py

class Sortting(object):
	u'''来自https://github.com/geekcomputers/Python.git的排序算法，感觉日后可能算法会用上，便先放进来存着以备后用
	'''
	def __init__(self, arg:list):
		self.__arg = arg
	
	@staticmethod
	def bubble_sort(nums):
		#TODO：新函数
		swapped = True
		while swapped:
			swapped = False
			for i in range(len(nums) - 1):
				if nums[i] > nums[i + 1]:
					# Swap the elements
					nums[i], nums[i + 1] = nums[i + 1], nums[i]
					# Set the flag to True so we'll loop again
					swapped = True
	
	@staticmethod
	def insertion_sort(nums):
		# TODO：新函数
		# Start on the second element as we assume the first element is sorted
		for i in range(1, len(nums)):
			item_to_insert = nums[i]
			# And keep a reference of the index of the previous element
			j = i - 1
			# Move all items of the sorted segment forward if they are larger than
			# the item to insert
			while j >= 0 and nums[j] > item_to_insert:
				nums[j + 1] = nums[j]
				j -= 1
			# Insert the item
			nums[j + 1] = item_to_insert
	
	@staticmethod
	def selection_sort(nums):
		# TODO：新函数
		# This value of i corresponds to how many values were sorted
		for i in range(len(nums)):
			# We assume that the first item of the unsorted segment is the smallest
			lowest_value_index = i
			# This loop iterates over the unsorted items
			for j in range(i + 1, len(nums)):
				if nums[j] < nums[lowest_value_index]:
					lowest_value_index = j
			# Swap values of the lowest unsorted element with the first unsorted
			# element
			nums[i], nums[lowest_value_index] = nums[lowest_value_index], nums[i]
	
	@staticmethod
	def merge(left_list, right_list):
		# TODO:新函数
		sorted_list = []
		left_list_index = right_list_index = 0
		
		# We use the list lengths often, so its handy to make variables
		left_list_length, right_list_length = len(left_list), len(right_list)
		
		for _ in range(left_list_length + right_list_length):
			if left_list_index < left_list_length and right_list_index < right_list_length:
				# We check which value from the start of each list is smaller
				# If the item at the beginning of the left list is smaller, add it
				# to the sorted list
				if left_list[left_list_index] <= right_list[right_list_index]:
					sorted_list.append(left_list[left_list_index])
					left_list_index += 1
				# If the item at the beginning of the right list is smaller, add it
				# to the sorted list
				else:
					sorted_list.append(right_list[right_list_index])
					right_list_index += 1
			
			# If we've reached the end of the of the left list, add the elements
			# from the right list
			elif left_list_index == left_list_length:
				sorted_list.append(right_list[right_list_index])
				right_list_index += 1
			# If we've reached the end of the of the right list, add the elements
			# from the left list
			elif right_list_index == right_list_length:
				sorted_list.append(left_list[left_list_index])
				left_list_index += 1
		
		return sorted_list
	
	@staticmethod
	def merge_sort(nums):
		# TODO：新函数
		# If the list is a single element, return it
		if len(nums) <= 1:
			return nums
		
		# Use floor division to get midpoint, indices must be integers
		mid = len(nums) // 2
		
		# Sort and merge each half
		left_list = merge_sort(nums[:mid])
		right_list = merge_sort(nums[mid:])
		
		# Merge the sorted lists into a new one
		return merge(left_list, right_list)