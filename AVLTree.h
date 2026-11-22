#pragma once

#include "TreeNode.h"
#include "AVLNode.h"
#include "Stack.h"
#include "DynamicArray.h"

#include <iostream>

template<typename T>
class AVLTree {
private:
    AVLNode<T>* root = nullptr;

    int getHeight(AVLNode<T>* node) {
        return node ? node->height : 0;
    }

    int getMax(int a, int b) {
        return a > b ? a : b;
    }

    int getBalanceFactor(AVLNode<T>* node) {
        if (!node) return 0;

        return getHeight(node->left) - getHeight(node->right);
    }

    void updateHeight(AVLNode<T>* node) {
        if (!node) return;

        node->height = 1 + getMax(getHeight(node->left), getHeight(node->right));
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

    AVLNode<T>* balance(AVLNode<T>* node) {
        if (!node) return nullptr;

        updateHeight(node);

        int balanceFactor = getBalanceFactor(node);

        if (balanceFactor > 1 && getBalanceFactor(node->left) >= 0) {
            return rotateRight(node);
        }

        if (balanceFactor > 1 && getBalanceFactor(node->left) < 0) {
            node->left = rotateLeft(node->left);
            return rotateRight(node);
        }

        if (balanceFactor < -1 && getBalanceFactor(node->right) <= 0) {
            return rotateLeft(node);
        }

        if (balanceFactor < -1 && getBalanceFactor(node->right) > 0) {
            node->right = rotateRight(node->right);
            return rotateLeft(node);
        }

        return node;
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

        return balance(node);
    }

    AVLNode<T>* findMin(AVLNode<T>* node) {
        while (node && node->left) {
            node = node->left;
        }

        return node;
    }

    AVLNode<T>* search(AVLNode<T>* node, T& value) {
        if (!node || node->value == value) {
            return node;
        }

        if (value < node->value) {
            return search(node->left, value);
        }

        return search(node->right, value);
    }

    AVLNode<T>* remove(AVLNode<T>* node, T& value) {
        if (!node) return nullptr;

        if (value < node->value) {
            node->left = remove(node->left, value);
        }
        else if (value > node->value) {
            node->right = remove(node->right, value);
        }
        else {
            if (!node->left) {
                AVLNode<T>* temp = node->right;
                delete node;
                return temp;
            }

            if (!node->right) {
                AVLNode<T>* temp = node->left;
                delete node;
                return temp;
            }

            AVLNode<T>* temp = findMin(node->right);

            node->value = temp->value;
            node->right = remove(node->right, temp->value);
        }

        return balance(node);
    }

    bool contains(AVLNode<T>* node, T& value) {
        if (!node) return false;

        if (value == node->value) return true;

        if (value < node->value) {
            return contains(node->left, value);
        }

        return contains(node->right, value);
    }

    void insertPreorder(TreeNode<T>* node) {
        if (!node) return;

        insert(node->value);

        insertPreorder(node->left);
        insertPreorder(node->right);
    }

    void clear(AVLNode<T>* node) {
        if (!node) return;

        clear(node->left);
        clear(node->right);

        delete node;
    }

public:
    AVLTree() = default;

    void build(TreeNode<T>* source) {
        clear(root);
        root = nullptr;

        insertPreorder(source);
    }

    AVLNode<T>* getRoot() {
        return root;
    }

    bool search(T& value) {
        return contains(root, value);
    }

    bool contains(T& value) {
        return contains(root, value);
    }

    void insert(T& value) {
        root = insert(root, value);
    }

    void remove(T& value) {
        root = remove(root, value);
    }

    int height() {
        return getHeight(root);
    }

    void printBFS() {
        if (!root) {
            std::cout << '\n';
            return;
        }

        DynamicArray<AVLNode<T>*> queue;

        queue.add(0, root);

        int index = 0;
        bool first = true;

        while (index < queue.size()) {
            AVLNode<T>* node = queue.get(index++);

            if (!first) std::cout << ", ";

            std::cout << node->value;
            first = false;

            if (node->left) {
                queue.add(queue.size(), node->left);
            }

            if (node->right) {
                queue.add(queue.size(), node->right);
            }
        }

        std::cout << '\n';
    }

    void printDFSPreorder() {
        Stack<AVLNode<T>> stack;

        if (root) {
            stack.push(root);
        }

        bool first = true;

        while (!stack.isEmpty()) {
            AVLNode<T>* node = stack.getFirstElement();
            stack.pop();

            if (!first) std::cout << ", ";

            std::cout << node->value;
            first = false;

            if (node->right) {
                stack.push(node->right);
            }

            if (node->left) {
                stack.push(node->left);
            }
        }

        std::cout << '\n';
    }

    void printDFSInorder() {
        Stack<AVLNode<T>> stack;

        AVLNode<T>* current = root;
        bool first = true;

        while (current || !stack.isEmpty()) {
            while (current) {
                stack.push(current);
                current = current->left;
            }

            current = stack.getFirstElement();
            stack.pop();

            if (!first) std::cout << ", ";

            std::cout << current->value;
            first = false;

            current = current->right;
        }

        std::cout << '\n';
    }

    void printDFSPostorder() {
        Stack<AVLNode<T>> stack;

        AVLNode<T>* current = root;
        AVLNode<T>* visited = nullptr;

        bool first = true;

        while (current || !stack.isEmpty()) {
            if (current) {
                stack.push(current);
                current = current->left;
            }
            else {
                AVLNode<T>* peek = stack.getFirstElement();

                if (peek->right && visited != peek->right) {
                    current = peek->right;
                }
                else {
                    if (!first) std::cout << ", ";

                    std::cout << peek->value;
                    first = false;

                    visited = peek;
                    stack.pop();
                }
            }
        }

        std::cout << '\n';
    }


    ~AVLTree() {
        clear(root);
    }
};
