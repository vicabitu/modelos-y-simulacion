import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import AppBar from '@mui/material/AppBar';
import FooterInfo from './FooterInfo';
import Chart from './Chart';
import CardInfo from './CardInfo';
import { useSimulation } from '../SimulationContext';

// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

export default function Dashboard() {
  const { simulationData } = useSimulation();
  console.log('Dashboard')
  console.log(simulationData)

  return (
    <ThemeProvider theme={defaultTheme}>
      <Box>
        <CssBaseline />
        <AppBar
          position="absolute"
          color="default"
          elevation={0}
          sx={{
            position: 'relative',
            borderBottom: (t) => `1px solid ${t.palette.divider}`,
          }}
        >
          <Toolbar>
            <Typography variant="h6" color="inherit" noWrap>
              Modelos y Simulación - Trabajo Practico Final
            </Typography>
          </Toolbar>
        </AppBar>
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Grid sx={{marginBottom: -5}}>
              <Typography variant="h5" gutterBottom>
                Datos de entrada:
              </Typography>
            </Grid>
              {simulationData?.map((data) => {
                return  (
                  <Grid key={data.anio} container spacing={2}>
                    <Grid item xs={12} md={12} lg={12} sx={{marginTop: 5}}>
                      <Typography variant="h5" gutterBottom>
                        {`Año: ${data.anio}`}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={4} lg={4}>
                      <Paper
                        sx={{
                          p: 2,
                          display: 'flex',
                          flexDirection: 'column',
                        }}
                      >
                        <CardInfo titulo='Produccion total en toneladas' valor={data.cantidadDeProduccionTotal} />
                      </Paper>
                    </Grid>
                    <Grid item xs={12} md={4} lg={4}>
                      <Paper
                        sx={{
                          p: 2,
                          display: 'flex',
                          flexDirection: 'column',
                        }}
                      >
                        <CardInfo titulo='Promedio de produccion (toneladas)' valor={data.promedioDeProduccion} />
                      </Paper>
                    </Grid>
                    <Grid item xs={12} md={4} lg={4}>
                      <Paper
                        sx={{
                          p: 2,
                          display: 'flex',
                          flexDirection: 'column',
                        }}
                      >
                        <CardInfo titulo='Promedio minutos sin materia prima' valor={data.promedioMinutosSinMateriaPrimaPorDia} />
                      </Paper>
                    </Grid>
                    <Grid item xs={12} md={12} lg={12}>
                      <Paper
                        sx={{
                          p: 2,
                          display: 'flex',
                          flexDirection: 'column',
                          height: 240,
                        }}
                      >
                        <Chart />
                      </Paper>
                    </Grid>
                  </Grid>
              )})}
            {/* Footer */}
            <Box sx={{marginTop: 8}} component="footer">
              <Typography variant="h6" align="center" gutterBottom>
                UNPSJB
              </Typography>
              <Typography
                variant="subtitle1"
                align="center"
                color="text.secondary"
                component="p"
              >
                Trabajo Practico Final
              </Typography>
              <FooterInfo />
            </Box>
            {/* End footer */}
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}
