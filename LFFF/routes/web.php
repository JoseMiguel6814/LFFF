<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\UserController;

Route::get('/', [UserController::class, 'inicio'])->name('usuario.inicio');

Route::post('/addUser', [UserController::class, 'store'])->name('usuario.store');

Route::get('/usuarios', [UserController::class, 'index'])->name('usuario.index');
