import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { VotacaoComponent } from './votacao/votacao.component';

const routes: Routes = [
  {path: '', component: VotacaoComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
