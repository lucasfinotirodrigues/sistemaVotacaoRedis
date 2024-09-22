import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class VotacaoService {
  private apiUrl = 'http://localhost:5000'; 

  constructor(private http: HttpClient) {}

  // Método para iniciar uma nova sessão de votação
  iniciarVotacao(sessaoData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/votacao/iniciar`, sessaoData);
  }

  // Método para listar as sessões de votação
  listarSessoes(): Observable<any> {
    return this.http.get(`${this.apiUrl}/votacao/sessoes`);
  }

  // Método para votar em uma pergunta específica
  votar(votoData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/votacao/votar`, votoData);
  }

  // Método para obter os resultados de uma sessão
  obterResultados(sessao: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/votacao/resultados/${sessao}`);
  }

  // Método para encerrar uma sessão de votação
  encerrarSessao(sessao: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/votacao/encerrar`, { sessao });
  }
}
