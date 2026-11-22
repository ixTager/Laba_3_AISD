#pragma once

#include "TreeNode.h"
#include "DynamicArray.h"
#include <iostream>

template<typename T>
class BinaryTree {
private:
    TreeNode<T>* root = nullptr;

    void preorder(TreeNode<T>* node, bool& first) {
        if (!node) return;

        if (!first) std::cout << ", ";

        std::cout << node->value;
        first = false;

        preorder(node->left, first);
        preorder(node->right, first);
    }

    void clear(TreeNode<T>* node) {
        if (!node) return;

        clear(node->left);
        clear(node->right);

        delete node;
    }

public:
    BinaryTree() = default;

    void add(T& value) {
        TreeNode<T>* newNode = new TreeNode<T>(value);

        if (!root) {
            root = newNode;
            return;
        }

        DynamicArray<TreeNode<T>*> queue;

        queue.add(queue.size(), root);

        while (queue.size() > 0) {
            TreeNode<T>* node = queue.get(0);
            queue.remove(0);

            if (!node->left) {
                node->left = newNode;
                return;
            }

            queue.add(queue.size(), node->left);

            if (!node->right) {
                node->right = newNode;
                return;
            }

            queue.add(queue.size(), node->right);
        }
    }

    TreeNode<T>* getRoot() {
        return root;
    }

    void printPreorder() {
        bool first = true;

        preorder(root, first);

        std::cout << '\n';
    }

    ~BinaryTree() {
        clear(root);
    }
};
