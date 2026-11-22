#pragma once

template<typename T>
struct AVLNode {
    T value;
    int height;
    AVLNode* left;
    AVLNode* right;

    AVLNode(T& val) : value(val), height(1), left(nullptr), right(nullptr) {}
};