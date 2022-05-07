import { configureStore } from "@reduxjs/toolkit"
import userReducer from './features/user'
import {TypedUseSelectorHook, useDispatch, useSelector } from "react-redux"
export const store = configureStore({
  reducer:{
    user:userReducer
  }
})

export type AppDispatch = typeof store.dispatch
export type RootState = ReturnType<typeof store.getState>

// declare type as global hooks at first, in case duplicated declaration within components
export const useAppDispatch = ()=>useDispatch<AppDispatch>()
export const useAppSelector:TypedUseSelectorHook<RootState> = useSelector