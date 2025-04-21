import os
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

driver = webdriver.Chrome()

results = []
screenshot_folder = "screenshots"
os.makedirs(screenshot_folder, exist_ok=True)

def take_screenshot(step):
    """Toma una captura de pantalla y la guarda en la carpeta especificada."""
    driver.save_screenshot(os.path.join(screenshot_folder, f"screenshot_{step}.png"))

def generate_html_report(results):
    """Genera un reporte HTML a partir de los resultados de las pruebas."""
    print("Generando reporte HTML...") 

    html = """
    <html>
    <head>
        <title>Reporte de Pruebas</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .success { color: green; }
            .fail { color: red; }
        </style>
    </head>
    <body>
        <h1>Reporte de Pruebas</h1>
        <table>
            <thead>
                <tr>
                    <th>Paso</th>
                    <th>Resultado</th>
                </tr>
            </thead>
            <tbody>
    """
    for result in results:
        html += f"""
            <tr>
                <td>{result['Paso']}</td>
                <td class="{ 'success' if result['Resultado'] == 'Éxito' else 'fail' }">{result['Resultado']}</td>
            </tr>
        """
    
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    report_path = "reporte_pruebas.html"
    with open(report_path, "w") as f:
        f.write(html)

    print(f"Reporte guardado en: {report_path}")  
try:
    driver.get("http://devsticket.rf.gd/index.html")
    take_screenshot("inicio")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "+ Agregar Ticket"))).click()
    time.sleep(1)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "titulo"))).send_keys("Ticket de Prueba")
    driver.find_element(By.ID, "descripcion").send_keys("Descripción del ticket de prueba.")
    driver.find_element(By.ID, "responsable").send_keys("Juan Pérez")
    driver.find_element(By.ID, "correo").send_keys("juan.perez@example.com")
    driver.find_element(By.ID, "prioridad").send_keys("Media")

    take_screenshot("formulario_llenado")

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    driver.execute_script("arguments[0].click();", submit_button)

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(2)

    take_screenshot("alerta_aceptada")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "list-group-item"))
    )
    time.sleep(1)
    tickets = driver.find_elements(By.CLASS_NAME, "list-group-item")

    ticket = None
    for t in tickets:
        if "Ticket de Prueba" in t.text:
            ticket = t
            break

    if ticket:
        results.append({"Paso": "Ticket creado visible en index", "Resultado": "Éxito"})
        take_screenshot("ticket_en_index")

        try:
            finalizar_btn = ticket.find_element(By.XPATH, ".//button[contains(text(),'Finalizar')]")
            finalizar_btn.click()
            results.append({"Paso": "Cambio de estado a finalizado", "Resultado": "Éxito"})
            take_screenshot("ticket_finalizado")
        except:
            results.append({"Paso": "Cambio de estado a finalizado", "Resultado": "Fallo: Botón no encontrado"})
            raise

        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Finalizados"))).click()
        time.sleep(2)

        take_screenshot("seccion_finalizados")

        finalizados = driver.find_elements(By.CLASS_NAME, "list-group-item")
        en_finalizados = any("Ticket de Prueba" in t.text for t in finalizados)

        if en_finalizados:
            results.append({"Paso": "Ticket visible en Finalizados", "Resultado": "Éxito"})
        else:
            results.append({"Paso": "Ticket visible en Finalizados", "Resultado": "Fallo"})

    else:
        results.append({"Paso": "Buscar ticket en index", "Resultado": "Fallo: No encontrado"})

except Exception as e:
    print("❌ Error durante la prueba:")
    traceback.print_exc()
    results.append({"Paso": "Error", "Resultado": str(e)})

finally:
    driver.quit()

    generate_html_report(results)
    print("✅ El reporte HTML ha sido generado.")
