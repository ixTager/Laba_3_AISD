#pragma once

template<typename T>
struct TreeNode {
	T value;
	TreeNode* left = nullptr;
	TreeNode* right = nullptr;

	TreeNode(T& val) : value(val) {}
};