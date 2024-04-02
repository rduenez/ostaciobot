/*
 * Created by SharpDevelop.
 * User: Omega
 * Date: 24/11/2011
 * Time: 11:36 a.m.
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using System.Windows.Forms;
using System.Drawing;

namespace Ostaciobot
{
	/// <summary>
	/// Class with program entry point.
	/// </summary>
	internal sealed class Program
	{
		/// <summary>
		/// Program entry point.
		/// </summary>
		[STAThread]
		private static void Main(string[] args)
		{
			Application.EnableVisualStyles();
			Application.SetCompatibleTextRenderingDefault(false);
			Application.Run(new MainForm());
		}
		
	}
	
	
	class MiPanel: Panel
	{
		MainForm v;
	
		public MiPanel(MainForm ventana)
		{
			//base();
			v=ventana;
		}
		
		protected override void OnPaint(PaintEventArgs e)
		{
			base.OnPaint(e);
			Graphics g = e.Graphics;
			
			for (int i=0;i<v.mapa.Length;i++)
			{
				for (int j=0;j<v.mapa[i].Length;j++)
				{
					if (v.mapa[i][j]==0)
						g.FillRectangle(Brushes.White,j*20,i*20,20,20);
					else if(v.mapa[i][j]==int.MaxValue)
						g.FillRectangle(Brushes.Black,j*20,i*20,20,20);
					else
						g.FillRectangle(Brushes.Gray,j*20,i*20,20,20);
					
					
					if (v.mapa[i][j]==-1)
					g.FillRectangle(Brushes.SkyBlue  ,j*20,i*20,20,20);
					
					if(i==v.posi && j ==v.posj)
					g.FillRectangle(Brushes.Sienna,j*20,i*20,20,20);
					
					g.DrawRectangle(Pens.Black,j*20,i*20,20,20);
				}
			}
			
		}
	}
}
