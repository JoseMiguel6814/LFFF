<?php
namespace App\Http\Controllers;
use App\Services\FastApiService;
use Illuminate\Http\Request;

class userController extends Controller
{
    protected $fastApi;
    public function __construct(FastApiService $fastApi)
    {
        $this->fastApi = $fastApi;
    }
    
    public function inicio()
    {
        return view('formulario');
    }
    
    public function store(Request $request)
    {
        $usuarioNuevo = $request->validate([
            'txtNombre' => 'required',
            'txtEdad' => 'required',
            'txtCorreo' => 'required',
        ]);
        
        $usuarioNuevo = [ 
            'name' => $usuarioNuevo['txtNombre'], 
            'age' => $usuarioNuevo['txtEdad'], 
            'email' => $usuarioNuevo['txtCorreo'], 
        ];
        try { 
            $response = $this->fastApi->post('/agregarusuariodb/', $usuarioNuevo);
            return redirect()->route('usuario.inicio')
                ->with('success', 'Usuario guardado por FASTAPI');
        } catch(Exception $e) {
            return back()->with('error', 'No fue posible guardar');
        }
    }
    
    public function index()
    {
        try {
            $usuarios = $this->fastApi->get('/todosusuarios/'); 
            return view('consulta', compact('usuarios'));
        } catch (\Exception $e) {
            return back()->with('error', 'No se pudo obtener la lista de usuarios');
        }
    }
}