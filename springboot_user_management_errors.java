// Main Application Class
@SpringBootApplication
@EnableJpaRepositories
@EnableScheduling
public class UserManagementApplication {
    public static void main(String[] args) {
        SpringApplication.run(UserManagementApplication.class, args);
    }
}

// User Entity - User.java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(unique = true, nullable = false)
    private String username;
    
    @Column(unique = true, nullable = false)
    private String email;
    
    @Column(nullable = false)
    private String password;
    
    @Enumerated(EnumType.STRING)
    private Role role;
    
    @CreationTimestamp
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    private LocalDateTime updatedAt;
    
    // Error: Missing @JsonIgnore on password field
    // Error: Missing constructors
    // Error: Missing getters/setters
    // Error: Missing equals/hashCode
}

// Role Enum
public enum Role {
    ADMIN, USER, MODERATOR
}

// UserDto Class - UserDto.java
public class UserDto {
    @NotBlank(message = "Username is required")
    private String username;
    
    @Email(message = "Invalid email format")
    @NotBlank(message = "Email is required")
    private String email;
    
    @Size(min = 8, message = "Password must be at least 8 characters")
    private String password;
    
    @NotNull(message = "Role is required")
    private Role role;
    
    // Error: Missing constructors, getters, setters
}

// Repository Interface - UserRepository.java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // Error: Should return Optional
    User findByUsername(String username);
    
    // Error: Should return Optional
    User findByEmail(String email);
    
    // Error: Wrong query syntax
    @Query("SELECT u FROM User u WHERE u.role = :role AND u.createdAt > :date")
    List<User> findActiveUsersByRole(@Param("role") Role role, @Param("date") LocalDateTime date);
    
    // Error: Missing @Modifying annotation
    @Query("UPDATE User u SET u.password = :newPassword WHERE u.id = :userId")
    void updateUserPassword(@Param("userId") Long userId, @Param("newPassword") String newPassword);
    
    // Error: Native query with wrong syntax
    @Query(value = "SELECT * FROM users WHERE created_at BETWEEN ?1 AND ?2", nativeQuery = true)
    List<User> findUsersByDateRange(LocalDateTime startDate, LocalDateTime endDate);
}

// Service Class - UserService.java
@Service
public class UserService {
    
    // Error: Field injection instead of constructor injection
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
    
    public User getUserById(Long id) {
        // Error: Not handling Optional properly
        return userRepository.findById(id).get();
    }
    
    public User createUser(UserDto userDto) {
        // Error: No duplicate check
        User user = new User();
        user.setUsername(userDto.getUsername());
        user.setEmail(userDto.getEmail());
        // Error: Not encoding password
        user.setPassword(userDto.getPassword());
        user.setRole(userDto.getRole());
        
        return userRepository.save(user);
    }
    
    public User updateUser(Long id, UserDto userDto) {
        // Error: No existence check
        User user = userRepository.findById(id).get();
        user.setUsername(userDto.getUsername());
        user.setEmail(userDto.getEmail());
        user.setRole(userDto.getRole());
        
        return userRepository.save(user);
    }
    
    public void deleteUser(Long id) {
        // Error: No existence check
        userRepository.deleteById(id);
    }
    
    // Error: Missing @Transactional
    public void changeUserPassword(Long userId, String newPassword) {
        userRepository.updateUserPassword(userId, passwordEncoder.encode(newPassword));
    }
    
    public User findByUsername(String username) {
        // Error: Not handling potential null
        return userRepository.findByUsername(username);
    }
}

// Controller Class - UserController.java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    // Error: Missing injection
    private UserService userService;
    
    @GetMapping
    public List<User> getAllUsers() {
        return userService.getAllUsers();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        // Error: No exception handling
        User user = userService.getUserById(id);
        return ResponseEntity.ok(user);
    }
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody UserDto userDto) {
        // Error: Missing @Valid annotation
        User user = userService.createUser(userDto);
        return ResponseEntity.ok(user);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(@PathVariable Long id, @Valid @RequestBody UserDto userDto) {
        User user = userService.updateUser(id, userDto);
        return ResponseEntity.ok(user);
    }
    
    @DeleteMapping("/{id}")
    public void deleteUser(@PathVariable Long id) {
        // Error: Should return ResponseEntity
        userService.deleteUser(id);
    }
    
    // Error: Missing @PostMapping
    public ResponseEntity<String> changePassword(@PathVariable Long id, @RequestBody String newPassword) {
        userService.changeUserPassword(id, newPassword);
        return ResponseEntity.ok("Password changed successfully");
    }
}

// Security Configuration - SecurityConfig.java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    // Error: Missing @Bean annotation
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
    
    // Error: Deprecated SecurityFilterChain configuration
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
                .antMatchers("/api/users/**").hasRole("ADMIN")
                .antMatchers("/api/public/**").permitAll()
                .anyRequest().authenticated()
            .and()
            .formLogin()
            .and()
            .httpBasic();
        
        return http.build();
    }
}

// User Details Service - CustomUserDetailsService.java
@Service
public class CustomUserDetailsService implements UserDetailsService {
    
    @Autowired
    private UserService userService;
    
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userService.findByUsername(username);
        
        // Error: No null check
        return org.springframework.security.core.userdetails.User.builder()
                .username(user.getUsername())
                .password(user.getPassword())
                .roles(user.getRole().name())
                .build();
    }
}

// Scheduled Tasks - ScheduledTasks.java
@Component
public class ScheduledTasks {
    
    private UserService userService;
    
    // Error: Missing @Scheduled annotation parameters
    @Scheduled
    public void cleanupInactiveUsers() {
        // Error: No actual cleanup logic
        System.out.println("Cleaning up inactive users...");
    }
    
    // Error: Wrong cron expression
    @Scheduled(cron = "0 0 12 * * *")
    public void generateDailyReport() {
        List<User> users = userService.getAllUsers();
        System.out.println("Daily report: " + users.size() + " users");
    }
}

// Exception Classes
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
}

public class DuplicateUserException extends RuntimeException {
    public DuplicateUserException(String message) {
        super(message);
    }
}

// Global Exception Handler - GlobalExceptionHandler.java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<String> handleUserNotFound(UserNotFoundException ex) {
        return ResponseEntity.notFound().build();
    }
    
    // Error: Missing @ExceptionHandler
    public ResponseEntity<String> handleDuplicateUser(DuplicateUserException ex) {
        return ResponseEntity.badRequest().body(ex.getMessage());
    }
    
    // Error: Wrong exception type
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<Map<String, String>> handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error -> 
            errors.put(error.getField(), error.getDefaultMessage())
        );
        return ResponseEntity.badRequest().body(errors);
    }
}

// Test Class - UserServiceTest.java
@SpringBootTest
public class UserServiceTest {
    
    @Autowired
    private UserService userService;
    
    // Error: Should be @MockBean
    @Mock
    private UserRepository userRepository;
    
    @Test
    public void testCreateUser() {
        UserDto userDto = new UserDto();
        userDto.setUsername("testuser");
        userDto.setEmail("test@example.com");
        userDto.setPassword("password123");
        userDto.setRole(Role.USER);
        
        // Error: No mock setup
        User result = userService.createUser(userDto);
        
        assertNotNull(result);
        assertEquals("testuser", result.getUsername());
    }
    
    @Test
    public void testGetUserById() {
        // Error: No mock setup
        User user = userService.getUserById(1L);
        assertNotNull(user);
    }
    
    // Error: Missing @Test annotation
    public void testDeleteUser() {
        userService.deleteUser(1L);
        // Error: No verification
    }
}

// Integration Test - UserControllerIntegrationTest.java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.ANY)
public class UserControllerIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Test
    public void testGetAllUsers() {
        // Error: No authentication setup
        ResponseEntity<List> response = restTemplate.getForEntity("/api/users", List.class);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }
}

// Application Properties - application.yml
server:
  port: 8080
  
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password: 
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.H2Dialect
  
  # Error: Missing security configuration
  security:
    user:
      name: admin
      password: admin
      roles: ADMIN
      
# Error: Missing logging configuration
logging:
  level:
    org.springframework.security: DEBUG
    
# Error: Missing management endpoints configuration
management:
  endpoints:
    web:
      exposure:
        include: health,info

# Maven Dependencies (partial pom.xml)
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    
    <!-- Error: Missing H2 dependency -->
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    
    <!-- Error: Missing security test dependency -->
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
</dependencies>