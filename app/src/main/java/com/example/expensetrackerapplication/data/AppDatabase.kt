package com.example.expensetrackerapplication.data

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(entities = [User::class, Expense::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun expenseDao(): ExpenseDao
}