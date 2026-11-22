#pragma once

#include "TreeNode.h"
#include "AVLNode.h"
#include <iostream>


template<typename T>
class AVLTree {
private:
    AVLNode<T>* root = nullptr;

    int getHeight(AVLNode<T>* node) {
        return node ? node->height : 0;
    }

    int max(int a, int b) {
        return a > b ? a : b;
    }

    int getBalanceFactor(AVLNode<T>* node) { return node ? getHeight(node->left) - getHeight(node->right) : 0; }

    void updateHeight(AVLNode<T>* node) {
        node->height = 1 + max(getHeight(node->left), getHeight(node->right));
    }

    AVLNode<T>* rotateRight(AVLNode<T>* y) {
        AVLNode<T>* x = y->left;
        AVLNode<T>* temp = x->right;

        x->right = y;
        y->left = temp;

        updateHeight(y);
        updateHeight(x);

        return x;
    }

    AVLNode<T>* rotateLeft(AVLNode<T>* x) {
        AVLNode<T>* y = x->right;
        AVLNode<T>* temp = y->left;

        y->left = x;
        x->right = temp;

        updateHeight(x);
        updateHeight(y);

        return y;
    }

    AVLNode<T>* insert(AVLNode<T>* node, T& value) {
        if (!node) {
            return new AVLNode<T>(value);
        }

        if (value < node->value) {
            node->left = insert(node->left, value);
        }
        else if (value > node->value) {
            node->right = insert(node->right, value);
        }
        else {
            return node;
        }

        updateHeight(node);

        int balance = getBalanceFactor(node);

        if (balance > 1 && value < node->left->value) {
            return rotateRight(node);
        }

        if (balance < -1 && value > node->right->value) {
            return rotateLeft(node);
        }

        if (balance > 1 && value > node->left->value) {
            node->left = rotateLeft(node->left);
            return rotateRight(node);
        }

        if (balance < -1 && value < node->right->value) {
            node->right = rotateRight(node->right);
            return rotateLeft(node);
        }

        return node;
    }

    void insertPreorder(TreeNode<T>* node) {
        if (!node) return;

        insert(node->value);
        insertPreorder(node->left);
        insertPreorder(node->right);
    }

    void preorder(AVLNode<T>* node) {
        if (!node) return;

        std::cout << node->value << ", ";
        preorder(node->left);
        preorder(node->right);
    }

    void inorder(AVLNode<T>* node) {
        if (!node) return;

        inorder(node->left);
        std::cout << node->value << ", ";
        inorder(node->right);
    }

    void postorder(AVLNode<T>* node) {
        if (!node) return;

        postorder(node->left);
        postorder(node->right);
        std::cout << node->value << ", ";
    }

    void clear(AVLNode<T>* node) {
        if (!node) return;

        clear(node->left);
        clear(node->right);
        delete node;
    }

public:
    void insert(T& value) {
        root = insert(root, value);
    }

    void build(TreeNode<T>* source) {
        insertPreorder(source);
    }

    int height() {
        return getHeight(root);
    }

    void printPreorder() {
        preorder(root);
    }

    void printInorder() {
        inorder(root);
    }

    void printPostorder() {
        postorder(root);
    }

    AVLNode<T>* getRoot() {
        return root;
    }

    ~AVLTree() {
        clear(root);
    }
};
