/*
 * MainForm.cs
 * 
 * Archivo con el punto de entrada de la rutina principal
 * 
 * Histórico:
 * 24/11/2011	roduenez	Creado
 * 
 * 
 *
 */
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace Ostaciobot
{
	/// <summary>
	/// Description of MainForm.
	/// </summary>
	public partial class MainForm : Form
	{
		/*Constantes Globales*/
		/// <summary>
		/// Marca en el mapa del objetivo
		/// </summary>
		public const int 	TARGET 		= -int.MaxValue;
		
		/// <summary>
		/// Marca en el mapa de traza de camino más corto
		/// </summary>
		public const int	SHORTPATH	= -int.MaxValue +1;	//Marcade camino corto
		
		/// <summary>
		/// Marca de casilla no visitada
		/// </summary>
		public const int	NOT_INIT 	= -1;				//Valor de control
		public const int	MOVES		= 4;				//num de movimientos
		public const int 	WALL		= int.MaxValue;		//pared
		
		public const int	UP 			= 0;			//movimientos
		public const int	LEFT 		= 1;
		public const int 	DOWN		= 2;
		public const int 	RIGHT		= 3;
		
		public const int	COLS 		= 50;		//columnas
		public const int	ROWS 		= 50;		//renglones
		public const int 	WALLS		= 500;		//paredes
		public const int 	MAXSTEPS	= 10000;	//carga de bateria
		public const int 	SEARCHSPEED	= 1;		//velocidad de busqueda
		public const int 	SHPATHSPEED	= 100;		//velocidad de marca de camino corto
				
		public Random r;						//generado de aleatorios

		public int ini_i			= 0; 		//valor inicial del robot en i
		public int ini_j			= 0;		//valor inicial del robot en i
		public int bateria			= MAXSTEPS; //bateria
		public int posi;						//posicion actual del robot en i
		public int posj;						//posicion actual del robot en j
		
		public int [][] mapa;					//mapa interno
		public int [][] mat_ady;				//matriz de caminos
		public int [] distancia;				//distancias
		public int [] anterior;					//registro donde queda orden de los nodos
		
		public List<int> direc;					//lista para ver movimientos disponibles
		
		public bool encontrado		= false;	//flag de busqueda
		public bool terminado		= false;	//flag de terminacion
		public bool [] visitado;				//arreglo para no repetir en camino corto
		
		//obtener numero lineal del nodo en su pos en el mapa
		public int GetLnPos(int r, int c){return COLS*r+c;}  
		
		//obtener el renglon o columna en el mapa de un nodo
		public int GetRow(int lp){return lp / COLS;}
		public int GetCol(int lp){return lp % COLS;}
		
		//constructor
		public MainForm()
		{
			//instancia de los objetos
			mapa = new int[ROWS][];
			direc=new List<int>();
			
			for (int i=0;i<ROWS;i++)
				mapa[i]=new int[COLS];
			
			mat_ady		=new int  [ROWS*COLS][];
			distancia	=new int  [ROWS*COLS];
			visitado	=new bool [ROWS*COLS];
			anterior	=new int  [ROWS*COLS];
			
			for (int i=0;i<ROWS*COLS;i++)
				mat_ady[i]=new int[MOVES];			
						
			InitializeComponent();
			InitializeValues();
			timer1.Start();

		}
		
		
		//inicializacion de los valores
		public void InitializeValues()
		{
			terminado=false;
			encontrado=false;
			bateria=MAXSTEPS;
			
			for (int i=0;i<ROWS;i++)
				for (int j=0;j<COLS;j++)
					mapa[i][j]= 0;
			
			for (int i=0;i<ROWS*COLS;i++)
			{
				distancia[i]=int.MaxValue;
				anterior[i]=NOT_INIT;
				visitado[i]=false;
			}
			
			for (int i=0;i<ROWS*COLS;i++)
				for (int j=0;j<MOVES;j++)					
					mat_ady[i][j]=int.MaxValue;
			
			r = new Random();
			
			ini_i = r.Next(ROWS);
			ini_j = r.Next(COLS);
			
			posi=ini_i;
			posj=ini_j;
			
			for (int i=0;i<WALLS;i++)
			{
				int barri = r.Next(ROWS);
				int barrj = r.Next(COLS);
				
				if(barri!=posi && barrj!=posj)
				mapa[barri][barrj]=WALL;
			}
						
			int di=0,dj=0;
			di = r.Next(ROWS);
			dj = r.Next(COLS);
			
			mapa[di][dj]=TARGET;
			timer1.Interval=SEARCHSPEED;
			timer1.Enabled=true;
		}
		
		//algoritmo de dijsktra para resolucion de camino mas corto
		public void camino(
							int or, 
							int des)
		{
			int actual		=	or;
			int menor		=	int.MaxValue;
			int dc 			= 	distancia[actual];
			int k			=	NOT_INIT;
			int nuevadist	=	int.MaxValue;
			int	ai;
			int aj;
			
			distancia[or]=0;
			anterior[or]=or;
			visitado[or]=true;
			
			while(actual!=des)
			{
				menor		= int.MaxValue;
				dc			= distancia[actual];
				nuevadist	= int.MaxValue;
				ai			= GetRow(actual);
				aj			= GetCol(actual);
				
				for(int i=0;i<COLS*ROWS;i++)
				{	
					if(visitado[i]==false)
					{
													
						if(i==actual-COLS)
						{
							if(mat_ady[actual][UP]==int.MaxValue)
								nuevadist = int.MaxValue;
							else
								nuevadist = dc+mat_ady[actual][UP];
						}
						else if(i==actual-1)
						{
							if(mat_ady[actual][LEFT]==int.MaxValue)
								nuevadist = int.MaxValue;
							else
								nuevadist = dc+mat_ady[actual][LEFT];
						}
						else if(i==actual+COLS)
						{
							if(mat_ady[actual][DOWN]==int.MaxValue)
								nuevadist = int.MaxValue;
							else
								nuevadist = dc+mat_ady[actual][DOWN];
						}
						else if (i==actual+1)
						{								
							if(mat_ady[actual][RIGHT]==int.MaxValue)
								nuevadist = int.MaxValue;
							else
								nuevadist = dc+mat_ady[actual][RIGHT];
						}
						else nuevadist=int.MaxValue;
						
						if(nuevadist<distancia[i])
						{							
							distancia[i]=nuevadist;
							anterior[i]=actual;
						}
						
						if(distancia[i]<menor)
						{
							menor=distancia[i];
							k=i;
						}
						
					}
				}
				actual=k;
				visitado[actual]=true;
			}
			MessageBox.Show("Camino mas corto encontrado en "+distancia[des]+" pasos",
			                "Camino mas corto",MessageBoxButtons.OK,MessageBoxIcon.Information);
		}
		
		
		//funcion que permite que el robot pueda conectar nodos aun cuando no los visita
		//de menera adyacente, si el robot visita 4 nodos juntos permite conectarlos		
		//   sin funcion               con funcion
		
		//   [  v  ][  <  ]         	[  v> ][ v<  ]
		//   [  >  ][  ^  ] 			[  ^> ][ ^<  ]
		public void sinOrden()
		{
			for (int i=0;i<ROWS;i++)
			{
				for (int j=0;j<COLS;j++)
				{
					for(int movs=0;movs<MOVES;movs++)
					{
						//busca que haya visita y no sea pared
						if (movs==UP) if(i > 0) 
							if(mapa[i-1][j]>0 && mapa[i-1][j] != WALL) mat_ady[GetLnPos(i,j)][UP]=1;
						if (movs==LEFT) if(j > 0) 
							if(mapa[i][j-1]>0 && mapa[i][j-1] != WALL) mat_ady[GetLnPos(i,j)][LEFT]=1;
						if (movs==DOWN) if(i < ROWS - 1) 
							if(mapa[i+1][j]>0 && mapa[i+1][j] != WALL) mat_ady[GetLnPos(i,j)][DOWN]=1;
						if (movs==RIGHT) if(j < COLS - 1) 
							if(mapa[i][j+1]>0 && mapa[i][j+1] != WALL) mat_ady[GetLnPos(i,j)][RIGHT]=1;
					}					
				}
			}
		}
			
		
		
		void Timer1Tick(
							object sender, 
							EventArgs e)
		{
			//fin de simulacion
			if (terminado)
			{
				timer1.Enabled=false;
				MessageBox.Show("Fin de la Simulacion","Fin",
				                MessageBoxButtons.OK,MessageBoxIcon.Information);
				if(MessageBox.Show("Desea iniciar una nueva simulacion?","Nueva simulacion",
				                   MessageBoxButtons.YesNo,MessageBoxIcon.Question)==DialogResult.Yes)
					InitializeValues();
				else
					this.Dispose();
				return;
			}
			
			//checar bateria			
			if(bateria<=-0)
			{
				timer1.Enabled=false;
				if(MessageBox.Show("La bateria se ha agotado, desea cambiar bateria?","Bateria Agotada",
				                   MessageBoxButtons.YesNo,MessageBoxIcon.Question)==DialogResult.Yes)
					bateria = MAXSTEPS;
				else
					terminado=true;
				timer1.Enabled=true;
				
				return;
			}
			
			//cuando encuentra el objetivo empieza a marcar el camino mas corto
			if (encontrado)
			{
				//termina de marca el camino
				if(posi == ini_i && posj == ini_j)
				{
					timer1.Enabled=false;
					MessageBox.Show("Seguimiento de camino mas corto terminado");
					terminado=true;
					timer1.Enabled=true;
					return;
				}	
				
				//marca en el mapa la ruta
				if (mapa[posi][posj]!=TARGET)
					mapa[posi][posj]=SHORTPATH;
				
				//obtiene el siguiente (anterior) nodo a marca
				int val=GetLnPos(posi,posj);
				int prev=anterior[val];
				
				//obtiene la columna y renglon del nodo
				posi=GetRow(prev);
				posj=GetCol(prev);
				
				bateria--;
			}
			else
			{
			
				//busca el objetivo o aumenta numero de visitas
				if(mapa[posi][posj]!=TARGET)
				{
					mapa[posi][posj]++;
				}
				else
				{
					//encuentr el objetivo
					timer1.Enabled=false;
					MessageBox.Show("Objetivo localizado");
					timer1.Interval=SHPATHSPEED;
					encontrado=true;
					sinOrden();
					camino(GetLnPos(ini_i,ini_j),GetLnPos(posi,posj));
					timer1.Enabled=true;
					return;
					
				}
				
				//indicador para mover a las casillas con menos visitas
				int menor =int.MaxValue;
				
				//encuentra las casillas con menor visita
				for(int movs=0;movs<MOVES;movs++)
				{
					if (movs==UP) if(posi > 0) if(mapa[posi-1][posj]<menor) menor=mapa[posi-1][posj];
					if (movs==LEFT) if(posj > 0) if(mapa[posi][posj-1]<menor) menor=mapa[posi][posj-1];
					if (movs==DOWN) if(posi < ROWS - 1) if(mapa[posi+1][posj]<menor)menor=mapa[posi+1][posj];
					if (movs==RIGHT) if(posj < COLS - 1) if(mapa[posi][posj+1]<menor)menor=mapa[posi][posj+1];
				}
				
				//limpia y genera una lista con las casillas menos visitadas
				direc.Clear();				
				for(int movs=0;movs<MOVES;movs++)
				{
					if (movs==UP) if(posi > 0) if(mapa[posi-1][posj]==menor) direc.Add(movs);
					if (movs==LEFT) if(posj > 0) if(mapa[posi][posj-1]==menor) direc.Add(movs);
					if (movs==DOWN) if(posi < ROWS - 1) if(mapa[posi+1][posj]==menor)direc.Add(movs);
					if (movs==RIGHT) if(posj < COLS - 1) if(mapa[posi][posj+1]==menor)direc.Add(movs);
				}
				
				//se genera aleatoriamente un movimiento a la lista de casillas poco visitadas
				int mov = direc[r.Next(direc.Count)];
			
				//se marca en la matriz de nodos la visita y se mueve el robot
				if (mov==UP) if(posi > 0){
					mat_ady[GetLnPos(posi,posj)][UP]=1;
					mat_ady[GetLnPos(posi-1,posj)][DOWN]=1;
					posi--;
				}
				if (mov==LEFT) if(posj > 0){
					mat_ady[GetLnPos(posi,posj)][LEFT]=1;
					mat_ady[GetLnPos(posi,posj-1)][RIGHT]=1;
					posj--;
				}
				if (mov==DOWN) if(posi < mapa.Length - 1){
					mat_ady[GetLnPos(posi,posj)][DOWN]=1;
					mat_ady[GetLnPos(posi+1,posj)][UP]=1;
					
					posi++;
				}
				if (mov==RIGHT) if(posj < mapa[0].Length - 1){
					mat_ady[GetLnPos(posi,posj)][RIGHT]=1;
					mat_ady[GetLnPos(posi,posj+1)][LEFT]=1;
					posj++;
				}
				
				bateria--;
			}
			
			this.Refresh();
		}
		
		
		protected override void OnPaint(
										PaintEventArgs e)
		{
			//esta funcion se llama con el refresh despues de los movimientos
			
			base.OnPaint(e);
			Graphics g = e.Graphics;
			
			
			float sw = (float)(this.Width-35)/(float)COLS; //largo de casilla
			float sh = (float)(this.Height-38)/(float)ROWS; //alto de casilla
			float sb = (float)(this.Height-80)/(float)MAXSTEPS;	//alto de bateria
		
			for (int i=0;i<ROWS;i++) //consulta de cada casilla
			{
				for (int j=0;j<COLS;j++)
				{
					if (mapa[i][j]==0)
						g.FillRectangle(Brushes.White,j*sw,i*sh,sw,sh);
					else if(mapa[i][j]==int.MaxValue)
						g.FillRectangle(Brushes.Black,j*sw,i*sh,sw,sh);
					else if (mapa[i][j]==SHORTPATH)
						g.FillRectangle(Brushes.Firebrick,j*sw,i*sh,sw,sh);
					else if (mapa[i][j]==TARGET)
						g.FillRectangle(Brushes.SteelBlue,j*sw,i*sh,sw,sh);
					else
						g.FillRectangle(Brushes.Gray,j*sw,i*sh,sw,sh);
					
					if(i==ini_i && j ==ini_j)
					g.FillRectangle(Brushes.ForestGreen,j*sw,i*sh,sw,sh);
					
					if(i==posi && j ==posj)
					g.FillRectangle(Brushes.Gold,j*sw,i*sh,sw,sh);
					
					g.DrawRectangle(Pens.Black,j*sw,i*sh,sw,sh);
				}
			}
			
			//dibujo de bateria
			g.FillRectangle(Brushes.Blue,this.Width-30,10,10,20);
			g.FillRectangle(Brushes.LightGray,this.Width-28,7,6,3);
			g.DrawString("+",new Font("Courier",10,FontStyle.Regular,GraphicsUnit.Pixel,0),Brushes.Yellow,this.Width-30,8);
			g.DrawString("_",new Font("Courier",10,FontStyle.Regular,GraphicsUnit.Pixel,0),Brushes.Yellow,this.Width-30,18);
			
			g.FillRectangle(Brushes.Red,this.Width-30,35,10,this.Height-80);
			g.FillRectangle(Brushes.Green,this.Width-30,35+((MAXSTEPS-bateria)*sb),
			                10,bateria*sb);
			
		}
	}
}
