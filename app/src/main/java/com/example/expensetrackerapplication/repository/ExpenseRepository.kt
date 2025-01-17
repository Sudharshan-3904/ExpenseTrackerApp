package com.example.expensetrackerapplication.repository


import com.example.expensetracker.data.Expense
import com.example.expensetracker.data.ExpenseDao

class ExpenseRepository(private val expenseDao: ExpenseDao) {
    fun getUserExpenses(userId: Int) = expenseDao.getUserExpenses(userId)

    suspend fun insertExpense(expense: Expense) {
        expenseDao.insertExpense(expense)
    }
}