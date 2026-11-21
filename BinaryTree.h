#pragma once
#include "TreeNode.h"

template <typename T>
class BinaryTree {
private:
    TreeNode<T>* root = nullptr;

    TreeNode<T>* getNode(TreeNode<T>* node, T& value) {
        if (node == nullptr) return nullptr;

        if (value == node->value) return node;
        if (value > node->value) return getNode(node->right, value);
        return getNode(node->left, value);
    }

    void setRoot(TreeNode<T>* newNode) {
        clear(root);
        root = newNode;
    }

    TreeNode<T>* add(TreeNode<T>* node, T& value) {
        if (node == nullptr) {
            return new TreeNode<T>(value);
        }
        if (value < node->value) {
            node->left = add(node->left, value);
        }
        else if (value > node->value) {
            node->right = add(node->right, value);
        }
        return node;
    }

    TreeNode<T>* findMin(TreeNode<T>* node) {
        while (node && node->left != nullptr) {
            node = node->left;
        }
        return node;
    }

    TreeNode<T>* remove(TreeNode<T>* node, T& value) {
        if (node == nullptr) return nullptr;

        if (value < node->value) {
            node->left = remove(node->left, value);
        }
        else if (value > node->value) {
            node->right = remove(node->right, value);
        }
        else {
            if (node->left == nullptr) {
                TreeNode<T>* temp = node->right;
                delete node;
                return temp;
            }
            else if (node->right == nullptr) {
                TreeNode<T>* temp = node->left;
                delete node;
                return temp;
            }

            TreeNode<T>* temp = findMin(node->right);
            node->value = temp->value;
            node->right = remove(node->right, temp->value);
        }
        return node;
    }

    void clear(TreeNode<T>* node) {
        if (node == nullptr) return;
        clear(node->left);
        clear(node->right);
        delete node;
    }

public:
    BinaryTree() = default;

    TreeNode<T>* dfs(T& value) {
        return getNode(root, value);
    }

    void add(T& value) {
        root = add(root, value);
    }

    void remove(T& value) {
        root = remove(root, value);
    }

    ~BinaryTree() {
        clear(root);
        root = nullptr;
    }
};
