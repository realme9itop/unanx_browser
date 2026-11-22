package com.unanx.browser.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface BookmarkDao {
    @Insert suspend fun insert(bookmark: BookmarkEntity)
    @Query("SELECT * FROM bookmarks ORDER BY timestamp DESC") fun getAll(): Flow<List<BookmarkEntity>>
    @Query("DELETE FROM bookmarks WHERE id = :id") suspend fun deleteById(id: Long)
}
